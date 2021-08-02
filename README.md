# optimal-detection

The gas dispersion study is used to predict whats happens if there is accidental gas leakage. This study using CFD allows knowing much information about the gas plumes, but how to lead with this information to obtain the best location for gas detectors?

Using this code you can obtain the optimal location for these detectors, this means that will be necessary a minimum quantity of detectors to cover all possible cases of studied leakage.

As input, you need to have a CSV archive as below:

Each line means one point in the CFD domain which can be a gas detector location. In the columns, we have the coordenates (X, Y, and Z) and the gas mass fraction value. For example, if you are analyzing 20 possible points to locate the detector and there are 5 different leakage cases (different gas sources, leakage direction, and/or wind directions), the CSV archive will have 20 * 5 = 100 lines because each case must be below the previous one.

There are three data that you need to change in the code: the number of cases, the number of points, and the mass fraction value that you want to detect. Follow the comments in the code to find where to put this information.
