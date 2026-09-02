# DIMM to RINGSS Upgrade

```{abstract}
Documentation regarding upgrading our Portable DIMM to a RINGSS instrument.
This is based on Andrei Tokovinin work, who has helped us designing this iteration.
```

## 1. Overview and Objective

The main goal is to transform the current **Portable DIMM (DIMM:2)** into a **RINGSS**-type seeing monitor (based on A. Tokovinin's design).

- **What is kept:** The current mount (**Astelco NTM-600**) and the optical tube assembly (**Photron 12" RC** / 304 mm Cassegrain).
- **What is replaced/upgraded:** The camera (replacing the Prosilica GC650C with one featuring higher quantum efficiency and lower read noise), the focuser, the internal optical train (aberration lenses to generate the ring pattern), and the acquisition and analysis software stack.

---

## 2. Equipment Logistics and Relocation

- **Transfer to La Serena:** Four boxes containing the OTA, camera, focuser, cables, controllers, and tools were measured and shipped from the Summit to the Electronics Lab in La Serena ([SUMMIT-12748](https://rubinobs.atlassian.net/browse/SUMMIT-12748), [SUMMIT-12750](https://rubinobs.atlassian.net/browse/SUMMIT-12750)).
- **Pending:** Final transfer of the full mount, tripod, and counterweights from the Summit to La Serena ([SUMMIT-13062](https://rubinobs.atlassian.net/browse/SUMMIT-13062)).

---

## 3. Optical Characterization of the Base Telescope

- **Aberration and Parameter Measurements:** Curvature Wavefront Sensing (CWFS) software and tests with distant point sources at Casa 8 were used to measure the telescope's intrinsic deformations ([RSO-164](https://rubinobs.atlassian.net/browse/RSO-164), [RSO-558](https://rubinobs.atlassian.net/browse/RSO-558)).
- **Zemax OpticStudio Model:** A precise telescope model (`304mmFinal.zmx`) was validated, confirming M1/M2 radii of curvature, conic constants, and systematic aberrations (Z₄ and Z₁₁).

---

## 4. Optical Design and Lens Configuration for RINGSS

- **Lens Selection:** Various lens combinations were simulated and evaluated in OpticStudio to generate the required aberrations (Z₄ ≈ −6.8 waves of defocus and Z₁₁ ≈ 0.62 waves of spherical aberration) ([RSO-165](https://rubinobs.atlassian.net/browse/RSO-165), [RSO-171](https://rubinobs.atlassian.net/browse/RSO-171)).
- **Optimal Configuration:** Use of an inverted achromatic doublet (e.g., Thorlabs **AC254-125-A** at 152.9 mm from the back plate and 59.44 mm from the CCD, or the LE1985-A + AC254-100-A combination), achieving:
  - Conjugate distance: **~1.2 km**
  - Effective focal length (EFL): **~1208.45 mm**
  - Ring geometry: **~20 pixels in diameter** and **3.3 to 4.5 pixels in width**

---

## 5. Hardware Selection and Integration

- **Camera ([RSO-166](https://rubinobs.atlassian.net/browse/RSO-166)):** The **Allied Vision Mako G-040B** was confirmed (monochrome CMOS sensor, high FPS on reduced regions of interest, 6.9 µm pixels, GigE PoE connection).
- **Focuser ([RSO-167](https://rubinobs.atlassian.net/browse/RSO-167)):** The **Optec TCF-Lynx** was selected (temperature-compensating focuser), requiring updates to `tt-scope` for command-based control.

---

## 6. Software Development, Numerical Models, and Documentation

- **Code Migration:** Simulation code migrated from IDL to **Python** ([RSO-240](https://rubinobs.atlassian.net/browse/RSO-240)).
- **Acquisition Software:** Development of the image acquisition and processing software for the new RINGSS camera ([RSO-241](https://rubinobs.atlassian.net/browse/RSO-241)).
- **Theoretical Model and Documentation:** Construction of the theoretical numerical model ([RSO-868](https://rubinobs.atlassian.net/browse/RSO-868)) and drafting of procedures, Tech Note, and project documentation ([RSO-189](https://rubinobs.atlassian.net/browse/RSO-189)).

---

*Full Epic: [RSO-163](https://rubinobs.atlassian.net/issues/?jql=parent%20%3D%20%22RSO-163%22%20ORDER%20BY%20created%20ASC)*


See the [Documenteer documentation](https://documenteer.lsst.io/technotes/index.html) for tips on how to write and configure your new technote.
