# Optimal-detection

The gas dispersion study is used to predict what happens if there is accidental gas leak. This study using CFD allows knowing specific details about the gas plumes. However, how can we take this information and obtain the best location for gas detectors?

Using this code you can have the optimal location for these detectors. This means that will be necessary a minimum quantity of detectors to cover all possible cases of studied leakage.

As input, you need to have a CSV archive as below:

![image](https://user-images.githubusercontent.com/88203900/128054833-d792c825-6d9c-4d8d-ac8d-d72936986410.png)

Each line means one point in the CFD domain which can be a gas detector location. In the columns, we have the coordinates (X, Y, and Z) and the gas mass fraction value. For example, if you are analyzing 20 possible points to locate the detector and there are 5 different leak cases (different gas sources, leakage direction, and/or wind directions), the CSV archive will have 20 * 5 = 100 lines because each case must be below the previous one.

Regarding input data, there are three data that you need to change in the code: the number of cases, the number of points, and the mass fraction value that you want to detect. Follow the comments in the code to find where to put this information.
