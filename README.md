# gpr-gym

## Introduction

This repo is an example of how one can generate many training examples with [gprMax](https://github.com/gprMax/gprMax)
 for use with machine learning models.
 The config is rough, but it should allow you to get started if you want to mass generate B-scans
 from [gprMax](https://github.com/gprMax/gprMax). As outlined in my [thesis](https://scholar.utc.edu/theses/595/),
 generating training data from [gprMax](https://github.com/gprMax/gprMax)
 on the scale necessary for the training of machine learning models
 can be difficult and was a major hurdle during my research. Hopefully this will allow you to
 get started with training data generation for your research. If you end up getting some benefit
 from this, I would appreciate it if you cite my thesis as one of the **Recommended Citations** below.
 Furthermore, feel free to reach out if you have any questions. I will do my best to answer them.

## Installation Instructions

    git clone --recursive git@github.com:will-rice/gpr-gym.git
    cd gprMax
    python setup.py build
    python setup.py install
    cd ..
    pip install -r requirements.txt

## Generate Training Data

    python generate_training_data.py

## Recommended Citations

This citation is recommended by the university

    Rice, William, "Applying generative adversarial networks to intelligent subsurface imaging and identification" (2019). Masters Theses and Doctoral Dissertations.
    <https://scholar.utc.edu/theses/595>

However, here is the arxiv bibtex if you prefer.

    @ARTICLE{2019arXiv190513321R,
           author = {{Rice}, William},
            title = "{Applying Generative Adversarial Networks to Intelligent Subsurface Imaging and Identification}",
          journal = {arXiv e-prints},
         keywords = {Electrical Engineering and Systems Science - Image and Video Processing, Computer Science - Machine Learning},
             year = "2019",
            month = "May",
              eid = {arXiv:1905.13321},
            pages = {arXiv:1905.13321},
    archivePrefix = {arXiv},
           eprint = {1905.13321},
     primaryClass = {eess.IV},
           adsurl = {<https://ui.adsabs.harvard.edu/abs/2019arXiv190513321R}>,
          adsnote = {Provided by the SAO/NASA Astrophysics Data System}
    }
