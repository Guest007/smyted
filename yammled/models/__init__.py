# -*- coding: utf-8 -*-

import fabric

print "Start..."


y_models = fabric.load_models()
print "Model 1: ", y_models[0]
print "Model 2: ", y_models[1]


print "Imported"