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

### lxplus

If you want to use bdt2cpp on CERNs lxplus machines, you need to get hold of
minimum python3.6. According to [CERNs Service Article
KB0000730](https://cern.service-now.com/service-portal/article.do?n=KB0000730),
one way to install the tool is:

```sh
# On lxplus
scl enable rh-python36

# this will install bdt2cpp to your `~/.local/` directory
pip install --user bdt2cpp
```

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

*Note for CERN Users*: Currently, the Makefile uses clang as the default
compiler. You might need to adjust that in the generated file (inside the
`build/` directory)

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
