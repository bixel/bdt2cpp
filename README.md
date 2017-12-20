# Generate C++ representations of boosted decision trees

This project tries to provide a generic functionality to transpile trained BDTs
into minimal, efficient C++ functions to evaluate single vectors of features.

While many frameworks exist to train, evaluate and store BDTs, its often hard
to use the results in a productive manner.

## Installation

So far there is only python3 support. Run
```
pip install bdt2cpp
```
to install the latest tagged version or
```
pip install git+https://github.com/bixel/bdt2cpp.git
```
for the current master version.

## Usage

To generate a minimal Makefile together with the C++ code inside a `build/`
directory from a given XGBoost dump or TMVA `.xml` file, simply run
```
bdt2cpp my-bdt-dump.xgb
```
You will find the corresponding files within the `build/` directory and if you
have installed `clang`, you can simply
```
cd build
make
```

The generated executable is essentially a very minimal placeholder, if you had
3 input features you could quickly cross-check the predictions against the
original training framework:
```
cd build
./main 1 2 3
```
should give the same output as received within the training framework if a
feature vector `f = (1, 2, 3)` is evaluated.


To see the complete list of features with some explanations, run
```
bdt2cpp -h
```
