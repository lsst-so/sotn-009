# DIMM to RINGSS Upgrade

```{abstract}
Documentation regarding our Portable DIMM to RINGSS upgrade.\
This is based on Andrei Tokovinin work, who has helped us designing this iteration.
```

## 1. Overview and Objective

In an era with ever-growing telescopes and cameras, reliable atmosphere monitors are necessary as ever. From DIMM to MASS these monitors have been constantly evolving, with different challenges and caveats in their construction and design. In the last decade, Andrei Tokovinin and collaborators introduced the Ring Image Next Generation Scintillation Sensor (RINGSS) as a new solution for turbulence profiling and atmosphere characterization.[]/
RINGSS combines a scintillation sensor and a motion monitor in a compact, as originally designed, 127mm from-shelf telescope, in combination with a set of lenses and a camera capable of over one-thousand frames per second in a relatively small region of interest[], all this to maintain a quick processing time and low-cost equipment.[] We then take this idea and tackle it with a question, "Can we develop a bigger diameter RINGSS?". We aim to upgrade an under-used DIMM telescope at Rubin (commonly refered to as Portable DIMM), and with minimal changes implement a RINGSS in a only-theorized 304mm telescope.[]


## 2. Theory

The straight-forward objective of these sky monitors is to measure and characterize how the atmosphere affects the quality of image we can achieve with our telescopes. The atmosphere can be divided in two main layers; the ground layer, where up to 2km we have most of turbulence caused by, redundantly, ground features and low wind, but not less important over these 2 km we have the free atmosphere, that is dominated by high winds and turbulence bubbles up to 30km where we have 99% of the atmosphere[]. From our position, we can only see this as a single flat screen *(right?)*. RINGSS takes a cube-image of a single defocused bright star and measures the Optical Turbulence Profile along our optical path.[]\
\
RINGSS works by measuring a defocused pupil image of the telescope. It introduces spherical aberrations through a calibrated set of lenses[], and physically creates a sharp conic wavefront focused on the radial axis[], hence the "Ring Image" part of the name. This ring image is both analyzed as a MASS instrument, taking the complete brightness variation into a scintillation sensor, and by dividing the ring into eight oppossed sectors, using DIMM-like processing to find a sector derived seeing[]. \
\
We take into account the Turbulence Profile, Fried parameter, Rytov variances, Kolmogorov power law, Weights of each layer, and derive windspeed, free atmosphere, sector seeing and scintilaltion seeing.

## 3. Simulations and models

Zemax: Out from schemas and simple measurements of the telescope, we were able to broadly design the optical model in Ansys' Zemax Optical Modelling software, where it let us test for different combination of lenses and cameras, thanks to manufacturer-provided lens models. This model was later reinforced by the optical characterization of the telescope through Xin and Claver's Curvature Wavefront Sensing scripts (CWFS github)[], as we found the native aberrations of the OTA without needing to disassemble it (and produce more aberrations). This images for the CWFS were taking at night, with two streetlights at 2 and 10 km, so they were point sources for the camera, a Prosilica GC650. \
Python: Andrei Tokovinin developed a Simulator to test possible configurations and check the modelling was correct for on-sky observations. Even though this was scripted in IDL, we translated the codes to Python 3.8 as faithful as possible, maintaining procedures, and adapting it to the different methods Python has, as well as making it more human readable and easy to test, both in CLI and in a Jupyter Notebook.\
(How does this sim work?)

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
