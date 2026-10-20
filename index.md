# DIMM to RINGSS Upgrade

```{abstract}
Documentation regarding upgrading our Portable DIMM to a RINGSS instrument.
This is based on Andrei Tokovinin work, who has helped us designing this iteration.
```

## 1. Overview and Objective

The main goal is to transform the current **Portable DIMM (DIMM:2)** into a **RINGSS**-type seeing monitor (based on A. Tokovinin's design).

- **What is kept:** The current mount (**Astelco NTM-600**) and the optical tube assembly (**Photron 12" RC** / 304 mm Cassegrain).
- **What is replaced/upgraded:** The camera (replacing the Prosilica GC650C with one featuring higher quantum efficiency and lower read noise), the focuser, the internal optical train (aberration lenses to generate the ring pattern), and the acquisition and analysis software stack.
- **Why a larger RINGSS?** (and how its affected differently)

---

## 2. Theory

Andrei Tokovinin developed the first iterationof the RINGSS, in its paper [Cite], where he talked about the posibility of a larger RINGSS than what he designed, so we enter to prove (or disprove) that a 304mm monitor is feasible and trust worthy, this would also prove all intermediate sizes, allowing institutions and observatories to give any unused telescope a new life.

(Here we reference papers)

---

## 3. Simulations and models

(From here we reference our own work)

---

## 4. Hardware and implementation

We characterized the bare OTA, where we found it's base aberrations and created the Zemax model following technical drawings from the manufacturer.
We also recieved a new camera that fits what we needed in Pixel Size and Image Speed, we also need to characterize this AV Mako G-040B.

---

## 5. Testing

Simulation: "If we measure the seeing correctly, it must not depend on the wind (in simulations)."
Hardware:

---

## 6. Conclusion

---

## 7. Future work

The acquisition software still needs to be created and implemented, as we only ran a dry-test.
We would like to have the telescope at 8th Floor, to compare straight with LSSTCam and its seeing measurements (DIMM-like, Donut Blur).

---

*Full Epic: [RSO-163](https://rubinobs.atlassian.net/issues/?jql=parent%20%3D%20%22RSO-163%22%20ORDER%20BY%20created%20ASC)*


See the [Documenteer documentation](https://documenteer.lsst.io/technotes/index.html) for tips on how to write and configure your new technote.
