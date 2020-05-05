## Raytracing in One Weekend
**Port to Python by Mauro Colella**
https://raytracing.github.io/books/RayTracingInOneWeekend.html

1200x960 (resampled, rendered at 1200x800)
100 aa samples
10 bounces (depth)
488 spheres
14 cores, i9 9900k
Python 3.7.4
Windows 10
----
Elapsed Time: 23:08:11.140

![Render](/render.png)

Aside from slow rendering, I observed discrepancies 
affecting the aspect ratio, and a different version 
of the equation for refraction. Put that in a todo 
and will handle it in a subsequent release.