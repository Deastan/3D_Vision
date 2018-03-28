# 3D_Vision - Lecture spring 2018

Bee Traffic sans Jassi mais avec Philipp et aussi julie

ETH Zurich - 3D Photography 2015
http://www.cvg.ethz.ch/teaching/3dphoto/
 

Description of the project

One problem a beekeeper can encounter during spring, is the sudden swarming of his bees. They do so to find a new location for their colony.

In this project we want to count the number of bees that enter and leave the hive at any particular time, to be able to detect such a bee swarming. Using a GoPro camera, we will take several short videos and apply background subtraction followed by segmentation using OpenCV to recognize the bees. To track the path of the bees in 3D, we will use OpenCV.

For the support of our project we found a paper \cite{paper}\relax which uses the tracking software 'SwarmSight' in combination with one camera for counting bees. 


Some problems we will encounter during the project are listed below:

- First of all, the hive has a brownish color, which causes a small difference in color between the bees and the hive. To facilitate the background subtraction we will put a coloured paper on the hive to better recognize the bees.
- Another challenge will be to detect the rapid movement of the bees for which we need a frame rate high enough to map the trajectory of the bees through the consecutive pictures.
- Furthermore we will have overlapping bees. Solving this issue will be complicated using a single camera. But since we are interested only in the number of bees this does not falsify our result if we confuse two bees with each other. Additionally if we are able to track the bees' paths using OpenCV then we could be be able to distinguish the bees from one another.
- We might not be able to distinguish bees from other insects. But we assume that this implies only a negligible error.


%Detailed descriptions of work packages you planned, their outcomes, the responsible group member and estimated timeline. Specify the challenges that will be tackled and considered solutions with possible alternatives, citing related documents if applicable. Mention the platform (Android, PC etc.) and the language (C++ etc.) you plan to use.

Outcomes and Demonstration

At the end of this project we want to be able to count the bees entering and leaving the hive. Furthermore we want to track the bees using a single camera. At the end of the semester we will demonstrate the results with recorded videos, on which the bees' path is tracked.
% Give detailed information on the expected outcome of your project and the experiments you plan to test your implementation. If applicable, describe the online or offline demo you plan to present at the end of the semester.



