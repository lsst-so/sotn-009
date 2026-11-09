# DIMM to RINGSS Upgrade

```{abstract}
Documentation regarding our Portable DIMM to RINGSS upgrade.
This is based on Andrei Tokovinin work, who has helped us designing this iteration.
```

## 1. Overview and Objective

In an era with ever-growing telescopes and cameras, reliable atmosphere monitors are necessary as ever. From DIMM to MASS these monitors have been constantly evolving, with different challenges and caveats in their construction and design. In the last decade, Andrei Tokovinin and collaborators introduced the Ring Image Next Generation Scintillation Sensor (RINGSS) as a new solution for turbulence profiling and atmosphere characterization.[]\
RINGSS combines a scintillation sensor and a motion monitor in a compact, as originally designed, 127mm from-shelf telescope, in combination with a set of lenses and a camera capable of over one-thousand frames per second in a relatively small region of interest[], all this to maintain a quick processing time and low-cost equipment.[] We then take this idea and tackle it with a question, "Can we develop a bigger diameter RINGSS?". We aim to upgrade an under-used DIMM telescope at Rubin (commonly refered to as Portable DIMM), and with minimal changes implement a RINGSS in a only-theorized 304mm telescope.[]


## 2. Theory

The straight-forward objective of these sky monitors is to measure and characterize how the atmosphere affects the quality of image we can achieve with our telescopes. The atmosphere can be divided in two main layers; the ground layer, where up to 2km we have most of turbulence caused by, redundantly, ground features and low wind, but not less important over these 2 km we have the free atmosphere, that is dominated by high winds and turbulence bubbles up to 30km where we have 99% of the atmosphere[]. From our position, the effect on the wavefront is the sum of every layer collapsed into a single distorted screen at the pupil. RINGSS takes a cube-image of a defocused bright single star and measures the Optical Turbulence Profile along our optical path.[]\
\
RINGSS works by measuring a defocused pupil image of the telescope. It introduces spherical aberrations through a calibrated set of lenses[], and physically creates a sharp conic wavefront focused on the radial axis[], hence the "Ring Image" part of the name. This ring image is both analyzed as a MASS instrument, taking the complete brightness variation into a scintillation sensor, and by dividing the ring into eight oppossed sectors, using DIMM-like processing to find a sector derived seeing[]. \
\
We take into account the Kolmogorov power law, Fried parameter, Rytov variances, Weights of each layer, Turbulence Profile and then derive windspeed, free atmosphere, sector seeing and scintilaltion seeing. In that order, they work as follows: \
- The Kolmogorov power law: (r^{-11/6} in the spatial-frequency domain) sets the statistics of the phase screen.\
- The Fried parameter r0: the single scalar that encodes the seeing for a given *turbulence integral J* (via J = 0.423*(2π/λ)^2*r0^{-5/3}, with seeing ∝ (J)^{0.6}).\
- The Rytov variance: it predicts how much scintillation a layer at a given height should produce and is used as a physical sanity check on the simulated screen.\
- The per-layer weights: pre-computed response functions that say how strongly each layer contributee to each measured angular mode.\

Then, if we take the weights and we invert them against the measured power spectrum (a non-negative least-squares fit) we get in return *the turbulence profile J(h)*. From that profile we find the total (scintillation) seeing by collapsing every layer, the free-atmosphere seeing by integrating only layers above 0.5 km, and the sector seeing independently from the radius-motion variance. Wind speed comes from how fast the scintillation pattern changes between consecutive frames. From the Fried Parameter r0 and the wind we then get the coherence time (tau) τ0, and from the profile's effective height the isoplanatic angle θ0.

## 3. Simulations and models

Zemax: Out from schemas and simple measurements of the telescope, we were able to broadly design the optical model in Ansys' Zemax Optical Modelling software, where it let us test for different combination of lenses and cameras, thanks to manufacturer-provided lens models. This model was later reinforced by the optical characterization of the telescope through Xin and Claver's Curvature Wavefront Sensing scripts (CWFS github)[], as we found the native aberrations of the OTA without needing to disassemble it (and produce more aberrations). This images for the CWFS were taking at night, with two streetlights at 2 and 10 km, so they were point sources for the camera, a Prosilica GC650.


Python: Andrei Tokovinin developed a Simulator to test possible configurations and check the modelling was correct for on-sky observations. Even though this was scripted in IDL, we translated the codes to Python 3.8 as faithful as possible, maintaining procedures, and adapting it to the different methods Python has, as well as making it more human readable and easy to test, both in CLI and in a Jupyter Notebook.

We can note that the complete RINGSS code separates in three sections; Acquisition, Restoration and Simulation. Currently we only take into account the two latter, as they are two sides of the complete pipeline (the Acquisition portion does not rely on the Simulation to work, and will be explained when we start on-sky testing), so we complete Andrei's on-sky half in Python with this Simulation port, allowing us to feed adapted values and conditions corresponding to our new RINGSS iteration into the simulation more automatically. Simply put, the simulation proceeds as follows:

1. *simatm* builds the atmosphere. From an input seeing it computes the Fried parameter r0 and the turbulence integral, splits it into a low and a high layer, and for each layer generates a Kolmogorov phase screen (r^{-11/6} spectrum scaled by 0.023^{1/2}) via an FFT. Then propagates the complex field layer-to-layer (starting at 16km, 8km, 4km and so on) and down to the ground with an angular-spectrum (Fresnel) step, so the output screen carries both the phase distortion and the height-dependent scintillation discussed in the Theory section. The field is saved to atm.npz, an image of it into the images folder, and as a diagnostic it prints the measured scintillation against the theoretical Rytov variance.\
2. *ringsim* then turns that screen into what the camera would see. It loads atm.npz, applies the telescope's annular pupil and the defocus/spherical wavefront (a4, a11) to form the ring, then slides the pupil across the screen frame by frame at the inputted wind speed, forming a time-resolved cube of ring images with photon (Poisson) and read-out (Gaussian) noise added. The cube is written as a FITS file, standing in for a real camera acquisition.\
3. *cubecoef* reduces the cube the same way that on-sky would: it finds the ring, centers every frame (sub-pixel Fourier shift), and projects each frame onto a set of sector and cos/sin angular masks to extract per-frame coefficients.\
4. *statmom* turns those per-frame coefficients into statistics.It finds the variance and one-frame-lag covariance of each angular mode (the power spectrum) and the differential radius variance of opposite sectors (the DIMM-like signal).\
5. *weights* computes, once per optical configuration, the altitude response functions (how strongly a layer at each height contributes to each measured mode) for two reference star colours, by the same Fresnel-propagation method used in simatm but run analytically per layer.\
6. *profrest* does the inversion: it noise-subtracts and saturation-corrects the measured power, fits it against the weights with a non-negative least-squares solver to recover the turbulence profile J(h), and from that profile reads out the scintillation (total), free-atmosphere and sector seeings, the wind speed, coherence time and isoplanatic angle.\
7. *testsimul* is the main script that calls all previous stages in sequence, then computes and stores the final measurements in a .csv file to analyze later, along with the inputs and outputs. autorunsimul only takes the testsimul driver, inputs what ever values we may want and runs several times the script.

## 4. Hardware and implementation

As the current Tower DIMM at Rubin, we are using an IOptron Ritchey-Chretien 12" OTA, in conjuntion with two ThorLabs lenses (which ones) at a distance of (X mm) between them, and (Y mm) to the camera, that as we said earlier is currently a new Allied Vision Mako G-040B Monochrome camera, with a detector of A x B pixels with 6.9 microns in size. This camera was/will be characterized to find the Read Out Noise and Spectral Response (?), and infront of it there will be installed two filters that constrain the incoming light from the telescope to only 400nm to 700nm (ThorLabs filters). The mount wasn't upgraded, as the Astelco NTM-600 is still a working piece, allowing the telescope to easily follow the stars in equatorial mode, reducing vibrations and movements from the mount that would be introduced to the camera and therefore acquisition and processing program. This configuration will/should be dry-tested on sky, with pending acquisition software and deployment to be fully constructed on 2027.

## 5. Testing

Simulation: "If we measure the seeing correctly, it must not depend on the wind (in simulations)."
Hardware:


## 6. Conclusion

We should expect similar results to those taken by R-DIMM and P-RINGSS

## 7. Future work

The acquisition software still needs to be created and implemented, as we only ran a dry-test.
We would like to have the telescope at 8th Floor, to compare straight with LSSTCam and its seeing measurements (DIMM-like, Donut Blur).


*Full Epic: [RSO-163](https://rubinobs.atlassian.net/issues/?jql=parent%20%3D%20%22RSO-163%22%20ORDER%20BY%20created%20ASC)*

## 8. Bibliography
See the [Documenteer documentation](https://documenteer.lsst.io/technotes/index.html) for tips on how to write and configure your new technote.

##
