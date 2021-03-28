# Pipeline Paper

Code to generate our paper explaining our work on our pipeline.

# Dependencies

You will need the following dependencies:

+ LaTeX compiler (Tested on texlive)
+ bibtex
+ Many LaTeX packages...
  + [IEEEconf](https://ctan.org/pkg/ieeeconf)

On Ubuntu, you can install all the other required packages by running
```bash
sudo apt install texlive texlive-latex-recommended \
  texlive-science texlive-publishers texlive-latex-extra  \
  texlive-bibtex-extra texlive-fonts-extra \
  biber
```
Or alternatively, (if you have a lot of disk space)
```bash
sudo apt install texlive-full bibtex
```

# Building

This project builds as a standard Makefile
