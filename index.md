# DIMM to RINGSS Upgrade

```{abstract}
Documentation regarding our Portable DIMM to RINGSS upgrade. This involved recreation of the optical model, translation and testing
of the numerical model from IDL to Python and characterization of hardware. 
This is based on Andrei Tokovinin work, who has helped us designing this iteration.
```

## 1. Overview and Objective

In an era with ever-growing telescopes and cameras, reliable atmosphere monitors are necessary as ever. From DIMM to MASS these monitors have been constantly evolving, with different challenges and caveats in their construction and design. In the last decade, Andrei Tokovinin and collaborators introduced the Ring Image Next Generation Scintillation Sensor (RINGSS) as a new solution for turbulence profiling and atmosphere characterization.[[4]](#bibliography) **Move this to abstract**

RINGSS combines a scintillation sensor and a motion monitor, as designed by Tokovinin, in a compact 127mm off-the-shelf telescope, in combination with a set of lenses and a camera capable of over one-thousand frames per second in a relatively small region of interest[[3]](#bibliography), all this to maintain a quick processing time and low-cost equipment.[[5]](#bibliography) We then take this idea and tackle it with a question, "Can we develop a bigger diameter RINGSS?". We aim to upgrade an under-used DIMM telescope at Rubin (commonly refered to as Portable DIMM or DIMM:2) ~with three objectives in mind;~ and with minimal changes implement a RINGSS in a only-theorized 304mm telescope.[[3]](#bibliography)

Even though we developed most part of python scripts, and the other half was already done by Andrei, we have not yet tested the telescope on-sky.

*Full Epic: [RSO-163](https://rubinobs.atlassian.net/issues/?jql=parent%20%3D%20%22RSO-163%22%20ORDER%20BY%20created%20ASC)*

## 2. Theory

The straight-forward objective of these sky monitors is to measure and characterize how the atmosphere affects the image quality we can achieve with our telescopes.[[7]](#bibliography) From the perspective of telescopes ~our position~, the effect on the wavefront is the sum of every atmospheric layer collapsed into a single distorted screen at the pupil. RINGSS takes series of images arranged in a datacube of a defocused bright single star and measures the Optical Turbulence Profile along it's optical path [[4]](#bibliography) in order to discretize the different layers of the atmosphere, the ground layer, close to us within 1 or 2 kilometers, and the free atmosphere, above the ground layer up to 16 kilomneters.

In other words, RINGSS works by measuring a defocused pupil image of the telescope main mirror. This instrument is mainly an evolution of a MASS-DIMM instrument developed earlier, which used a convoluted set of lenses and mirrors to combine DIMM and MASS capabilities, in contrast, we introduce spherical aberrations through (one or two) lenses[[4]](#bibliography), to physically create a sharp conic wavefront focused on the radial axis[[4]](#bibliography), hence the "Ring Image" part of the name. This ring image reveals, via how the ring moves, the turbulence-caused variations along each layer of the atmosphere, and is both analyzed as an analogue to the MASS instrument, taking the complete brightness variation into a scintillation sensor, and by dividing the ring into eight oppossed sectors, using DIMM-like processing to find a sector derived seeing[[1]](#bibliography). Henceforth, we need this focused ring, caused by the aberrations introduced, to have a relatively small width for high enough contrast. 

We take into account the Kolmogorov power law, Fried parameter, Rytov variances, Weights of each layer, Turbulence Profile and then derive wind speed, free atmosphere, sector seeing and scintilaltion seeing. In that order, they work as follows: 
- **The Kolmogorov power law:** ($r^{-11/6}$ in the spatial-frequency domain) sets the statistics of the phase screen.
- **The Fried parameter:** the single scalar that encodes the seeing for a given *turbulence integral J* (via $J = 0.423\,(2\pi/\lambda)^2\,r_0^{-5/3}$, with $\mathrm{seeing} \propto J^{0.6}$).
- **The Rytov variance:** ($\sigma_R^2 = 19.22\,\lambda^{-7/6}\sum_i z_i^{5/6}\,J_i$) it predicts how much scintillation a layer at a given height should produce and is used as a physical sanity check on the simulated screen.
- **The per-layer weights:** ($W_m(z) \propto \sin^2(\pi\lambda z f^2)$) pre-computed response functions that say how strongly each layer contributee to each measured angular mode.

Then, if we take the weights and we invert them against the measured power spectrum (a non-negative least-squares fit) we get in return *the turbulence profile J(h)* (J0...J16) (h being the layer/altitude). From that profile we find the total (scintillation) seeing (see, fwhmScintillation) by collapsing every layer, the free-atmosphere seeing (fsee, fwhmFree) by integrating only layers above an arbitrarily selected kilometer, and the sector seeing (see2, fwhmSector) from the radius-motion variance. Wind speed (wind) comes from how fast the scintillation pattern changes between consecutive frames. From the Fried Parameter r0 and the wind we then get the coherence time (tau) τ0 $(\tau_0 = 0.31\,r_0/\bar{v})$ (tau0), and from the profile's effective height the isoplanatic angle (theta) θ0 $(\theta_0 = 0.31\,r_0/\bar{h})$ (theta0).

## 3. Simulations and models

### Zemax
Out from manufacturer-sourced schemas and simple measurements of the telescope, we were able to broadly design the optical model in Ansys' Zemax Optical Modelling software, where it let us test for different combination of lenses and cameras, thanks to lens models provided by ThorLabs or Edmund Optics. This model was later reinforced by the optical characterization of the telescope through Xin and Claver's Curvature Wavefront Sensing scripts[[8]](#bibliography), as we found the native aberrations of the OTA without needing to disassemble it (and produce more aberrations). The images taken for the CWFS software should be taken at night and with point-source stars, but at the moment of this testing there was the on-going August 2026 temporal, so we didn't have the mount at our disposition. We improvised these point-sources with streetlight lamps at 2km and 10km, taking into account the distance and size of each they were point-sources for the telescope configuration, with a 7.4 µm pixel Prosilica GC650 camera.

(Zemax Image)

### Python
Andrei Tokovinin developed a Simulator to test possible configurations and check the modelling was correct for on-sky observations.[[6]](#bibliography) Even though this was scripted in IDL, we translated the codes to Python 3.8 as close as possible, maintaining procedures, and adapting it to the different methods Python has, as well as making it more human readable and easy to test, both in Command Line Interface (CLI) and in a Jupyter Notebook.

We can note that the complete RINGSS code separates in three sections; Acquisition, Restoration and Simulation. Currently we only take into account the two latter, as they are two sides of the complete pipeline (the Acquisition portion does not rely on the Simulation to work, and will be explained when we start on-sky testing), so we complete Andrei's on-sky half in Python with this Simulation port, allowing us to feed adapted values and conditions corresponding to our new RINGSS iteration into the simulation more automatically. Simply put, the simulation proceeds as follows:

1. `simatm.py` builds the atmosphere. From an input seeing it computes the Fried parameter `r0` and the turbulence integral, splits it into a low and a high layer, and for each layer generates a Kolmogorov phase screen ($r^{-11/6}$ spectrum scaled by $0.023^{1/2$}) via a Fast Fourier Transform. Then propagates the complex field layer-to-layer (starting at 16km, 8km, 4km and so on) and down to the ground with an angular-spectrum (Fresnel) step, so the output screen carries both the phase distortion and the height-dependent scintillation discussed in the Theory section. The field is saved to `atm.npz`, an image of it into the images folder, and as a diagnostic it prints the measured scintillation against the theoretical Rytov variance.
2. `ringsim.py` then turns that screen into what the camera would see. It loads `atm.npz`, applies the telescope's annular pupil and the defocus/spherical wavefront `(a4, a11)` to form the ring, then slides the pupil across the screen frame by frame at the inputted wind speed, forming a time-resolved cube of ring images with photon (Poisson) and read-out (Gaussian) noise added. The cube is then written as a FITS file, standing in for a real camera acquisition data cube.
3. `cubecoef.py` reduces the cube the same way that on-sky would: it finds the ring, centers every frame (sub-pixel Fourier shift), and projects each frame onto a set of sector and cos/sin angular masks to extract per-frame coefficients.
4. `statmom.py` turns those per-frame coefficients into statistics. It finds the variance and one-frame-lag covariance (statistical moments) of each angular mode (the power spectrum) and the differential radius variance of opposite sectors (the DIMM-like signal).
5. `weights.py` computes, once per optical configuration, the altitude response functions (how strongly a layer at each height contributes to each measured mode) for two reference star colours, by the same Fresnel-propagation method used in simatm but run analytically per layer.
6. `profrest.py` does the inversion: it noise-subtracts and saturation-corrects the measured power, fits it against the weights with a non-negative least-squares (`nnls`) solver to recover the turbulence profile `J(h)`, and from that profile reads out the scintillation (total), free-atmosphere and sector seeings, the wind speed, coherence time and isoplanatic angle.
7. `testsimul.py` is the main script that calls all previous stages in sequence, then computes and stores the final measurements in a `.csv` file to analyze later, along with the inputs and outputs. `autorunsimul.py` only takes the `testsimul.py` driver, inputs values hard-coded or from a parameter file and runs several times the script.

## 4. Hardware and implementation

As the current Tower DIMM at Rubin, we are using an IOptron Ritchey-Chretien 12" OTA, in conjuntion with a 25.4 mm Ø and 125 mm Focal length ThorLabs lens at a distance of 152.9 mm from the backplate and at 59.44 mm to the camera, that as we said earlier is currently a new Allied Vision Mako G-040B Monochrome camera, with a CMOS detector of 728 x 544 pixels with 6.9 microns in size, but to achieve the 1000 FPS needed we only use a 64x64 ROI. This camera should be characterized to find the Read Out Noise and Spectral Response, and infront of it there will be installed two filters that constrain the incoming light from the telescope to only 400nm to 700nm (FESH0700 + FELH0550 ThorLabs filters). The mount wasn't upgraded, as the Astelco NTM-600 is still a working piece, allowing the telescope to easily follow the stars in equatorial mode, reducing vibrations and movements from the mount that would be introduced to the camera, therefore to the acquisition and processing program. This configuration will be dry-tested on sky, with pending acquisition software and fully deployed on 2027.

(IRL Image)

## 5. Testing

We tested the Python port against real on-sky samples, feeding the Pachon RINGSS **sector** seeing[[5]](#bibliography) as the simulation input and comparing each recovered channel against its matched Pachon measurement (1355 matched samples, 0.45–3.5"). With the caveat that no two monitors calibrate exactly against each other due to inherent biases, we look for the trend each channel follows:

- **Sector seeing** (`see2`, `fwhmSector`) tracks its input almost 1:1 — R ≈ 0.99, mean ratio 0.99 against the Pachon sector seeing (R ≈ 0.93 against the co-located DIMM). This robust DIMM-like channel recovers the input faithfully.
- **Scintillation seeing** (`see`, `fwhmScintillation`) sits ~20% below the sector *input* (ratio ≈ 0.79), but this is the expected physical gap between the scintillation and sector channels, not a simulation error: against the Pachon *scintillation* seeing — the correct like-for-like reference — it matches almost exactly (R ≈ 0.99, ratio ≈ 1.01). The simulation reproduces the real scintillation channel.
- **Free-atmosphere seeing** (`fsee`, `fwhmFree`) correlates with the Pachon free-atmosphere seeing (R ≈ 0.83) but runs ~20% high (ratio ≈ 1.20), and is the noisiest of the three.
- **Wind speed** (`wind`, `wind`) is effectively decoupled from the real wind (R ≈ 0.14, sitting ~14 m/s regardless of input), consistent with Andrei Tokovinin's note that, with a single uniformly-translated phase screen (frozen flow), the recovered wind is not a meaningful quantity in these simulations.

In short, the sector and scintillation seeings reproduce their matched on-sky channels to within a few percent, the free-atmosphere channel is biased ~20% high, and the wind is independent due to modelling.

## 6. Conclusion

(ToDo - Conclusion + Future work)

## 7. Future work

- The acquisition software still needs to be created and implemented, as we only ran a dry-test.
- We would like to have the telescope at 8th Floor, to compare straight with LSSTCam and its seeing measurements (DIMM-like, Donut Blur).
- The Mako G-040B camera still needs to be characterized, as this impacts how the instrument works.

## 8. Bibliography

1. [From Differential Image Motion to Seeing](https://github.com/lsst-so/sotn-009/blob/main/archive/From%20Differential%20Image%20Motion%20to%20Seeing.pdf)
2. [Model of optical turbulence profile at Cerro Pachón](https://github.com/lsst-so/sotn-009/blob/main/archive/Model%20of%20optical%20turbulence%20profile%20at%20Cerro%20Pachon.pdf)
3. [RINGSS turbulence sensor based on Celestron Nexstar 5SE](https://github.com/lsst-so/sotn-009/blob/main/archive/RINGSS%20turbulence%20sensor%20based%20on%20Celestron%20Nexstar%205SE.pdf)
4. [Measurement of turbulence profile from defocused ring images](https://github.com/lsst-so/sotn-009/blob/main/archive/Measurement%20of%20turbulence%20profile%20from%20defocused%20ring%20images.pdf)
5. [Site monitor based on the RINGSS concept](https://github.com/lsst-so/sotn-009/blob/main/archive/Site%20monitor%20based%20on%20the%20RINGSS%20concept.pdf)
6. [Python software for turbulence measurements with RINGSS](https://github.com/lsst-so/sotn-009/blob/main/archive/Python%20software%20for%20turbulence%20measurements%20with%20RINGSS.pdf)
7. [The elusive nature of seeing](https://github.com/lsst-so/sotn-009/blob/main/archive/The%20elusive%20nature%20of%20seeing.pdf)
8. [CWFS Github repository](https://github.com/bxin/cwfs)


(ToDo - Add images)

See the [Documenteer documentation](https://documenteer.lsst.io/technotes/index.html) for tips on how to write and configure your new technote.

##
