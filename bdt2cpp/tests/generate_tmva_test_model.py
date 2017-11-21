#! /usr/bin/env python
""" Generate a dummy TMVA BDT model, following this blog post
https://aholzner.wordpress.com/2011/08/27/a-tmva-example-in-pyroot/
and this bug report... https://root-forum.cern.ch/t/factory-object-has-no-attribute-addvariable-in-tmva-python/25090/4
"""

import ROOT
from ROOT import TMVA

import root_pandas
import pandas as pd


# create a TNtuple
ntuple = ROOT.TNtuple('ntuple', 'ntuple', 'x:y:signal')

# generate 'signal' and 'background' distributions
for i in range(10000):
    # throw a signal event centered at (1,1)
    ntuple.Fill(ROOT.gRandom.Gaus(1,1), ROOT.gRandom.Gaus(1,1), 1)

    # throw a background event centered at (-1,-1)
    ntuple.Fill(ROOT.gRandom.Gaus(-1,1), ROOT.gRandom.Gaus(-1,1), 0)


output_file = ROOT.TFile('test.root', 'RECREATE')
tmva_options = ':'.join([
    '!V',
    '!Silent',
    'Color',
    'DrawProgressBar',
    'Transformations=I;D;P;G;D',
    'AnalysisType=Classification',
    ])

factory = TMVA.Factory('TMVAClassification', output_file, tmva_options)
dataloader = TMVA.DataLoader('dataset')
dataloader.AddVariable('x')
dataloader.AddVariable('y')
dataloader.AddSignalTree(ntuple)
dataloader.AddBackgroundTree(ntuple)

sigCut = ROOT.TCut('signal > 0.5')
bkgCut = ROOT.TCut('signal <= 0.5')

prepare_options = ':'.join([
    'nTrain_Signal=0',
    'nTrain_Background=0',
    'SplitMode=Random',
    'NormMode=NumEvents',
    '!V',
    ])
dataloader.PrepareTrainingAndTestTree(sigCut, bkgCut, prepare_options)

bdt_options = ':'.join([
    '!H',
    '!V',
    'NTrees=2',
    'nEventsMin=150',
    'MaxDepth=1',
    'BoostType=AdaBoost',
    'AdaBoostBeta=0.5',
    'SeparationType=GiniIndex',
    'nCuts=20',
    'PruneMethod=NoPruning',
    ])
factory.BookMethod(dataloader, TMVA.Types.kBDT, 'BDT', bdt_options)

factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
