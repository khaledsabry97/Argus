<!-- PROJECT LOGO -->
<br />

  <h1 align="center">ARGUS</h1>
<p align="center">
  <img src="Images\logo.png">
</p>

  <p align="center">
An autonomous system based on computer vision techniques that detects road accidents and reports them in real-time as well as allowing the monitoring of accidents using a client server architecture and an interactive GUI.    <br />
    <a href="https://github.com/khaledsabry97/Argus/blob/master/Documents/GP_document.pdf"><strong>Explore Full Documentation »</strong></a>
    <br />
    <br />
    <a href="IEEE-Research">IEEE Research Paper</a>
    .
    <a href="#ieee-conference-presentation-video">IEEE Presentation</a>
    ·
    <a href="#Demo">View Demo</a>
    ·
    <a href="#System-Architecture">System Architecture</a>
    ·
    <a href="https://github.com/khaledsabry97/Argus/issues">Request Feature</a>
  </p>

<p align="center">
 
<img src="https://github.com/khaledsabry97/Argus/blob/master/Gif/1517.gif?raw=true" width="200" height="200" />
<img src="https://github.com/khaledsabry97/Argus/blob/master/Gif/1518.gif?raw=true" width="200" height="200" />
<img src="https://github.com/khaledsabry97/Argus/blob/master/Gif/1519.gif?raw=true" width="200" height="200" />
<img src="https://github.com/khaledsabry97/Argus/blob/master/Gif/1529.gif?raw=true" width="200" height="200" />
<img src="https://github.com/khaledsabry97/Argus/blob/master/Gif/1566.gif?raw=true" width="200" height="200" />
<img src="https://github.com/khaledsabry97/Argus/blob/master/Gif/1522.gif?raw=true" width="200" height="200" />
<img src="https://github.com/khaledsabry97/Argus/blob/master/Gif/1528.gif?raw=true" width="200" height="200" />
<img src="https://github.com/khaledsabry97/Argus/blob/master/Gif/1568.gif?raw=true" width="200" height="200" />
 </p>

  <h2 id="IEEE-Research">
IEEE Research Paper</h2>


  <p> 
    This paper proposes a framework to detect road accidents in real-time using generic CCTV cameras installed on roads. The framework focuses on how to achieve high performance on congested roads by introducing a new technique called track-compensated frame interpolation (TCFI) for tracking the vehicles, focuses on achieving higher accuracy by introducing a new approach for crash detection called crash estimation algorithm and focuses on how the system will deal with the massive number of CCTV cameras by dropping footages that are highly unlikely to contain an accident at an early stage and implemented the modules based on the pipelining technique. The framework is formed up of four stages; first, vehicles are detected using YOLO neural network, then tracked for several frames using MOSSE tracker, followed by a filtration process based on a new approach of crash estimation; finally, for every vehicle, we process its tracked footage through ViF descriptor then use the output as a feature vector for an SVM model that classifies accidents. The system achieves 93% accuracy with processing time beats all previous systems.
  </p>
  <h4><a href="https://ieeexplore.ieee.org/document/9698968/">
Research Paper On IEEE </h4>
<h5 id="IEEE-Cite">
Citation</h5>

```
K. Sabry and M. Emad, "Road Traffic Accidents Detection Based On Crash Estimation," 2021 17th International Computer Engineering Conference (ICENCO), 2021, pp. 63-68, doi: 10.1109/ICENCO49852.2021.9698968.
  
```

  <h2 id="System-Architecture">
System Architecture
</h2>


<p align="center">
<img src="https://github.com/khaledsabry97/Argus/blob/master/Images/BlockDiagram.png" width="80%">
      </a>
  </p>
 


  <h2 id="Framework-Architecture">
Framework Architecture
</h2>

<p> The framework consists of 4 phases; it starts with a vehicle detection phase using YOLO architecture. The second phase is the vehicle tracking using MOSSE tracker. Then the third phase is a new approach we introduce to detect crash based on crash estimation. Finally, we can consider either what remains after the third phase is a crash or start the fourth phase, crash detection using violent flow descriptor. </p>

<p align="center">
<img src="https://github.com/khaledsabry97/Argus/blob/master/Images/framework.png" width="80%">
      </a>
  </p>





## How to Run Argus
1. Install requirements.txt
1. Run Backend Services
   1. RunMaster.py
   1. RunDetect.py
   1. RunTracker.py
   1. RunCrash.py
1. Run Client Services
   1. RunGui.py
   1. RunCamera.py
1. Select video from videos folder
1. From RunCamera.py hit Process

## How to Configure used modules in Project
As the project has different settings there are hyper-parameter you need to configure to use the module you actually want. Go to file called "Constants.py" in "Argus/System/Data/Constants.py"

 <details>
  <summary><b>In Detection Module</b></summary>
   <ul>
    <li> Work_Detect_Files : True if you want to use already saved vehicles detected in the videos provided in project instead of using YOLO architecture</li>
     </ul>
         </details>
         
 <details>
  <summary><b>In Tracking Module</b></summary>
  <ul>
    <li> Work_Tracker_Type_Mosse : True if you want to use Mosse Tracker instead of Dlib Tracker </li>
    <li> Work_Tracker_Interpolation : True if you want to use track-compensated frame interpolation (TCFI) instead of normal tracking algorithm
 </li>
    </ul>
         </details>
         
         
 <details>
  <summary><b>In Crash Module</b></summary>
   <ul>
    <li> Work_Crash_Estimation_Only : True if you want to use Crash Estimation Module Only, instead of following the Crash Estimation Module with ViF Descripton</li>
     </ul>
         </details>


## IEEE Conference Presentation Video
<p align="center" id="IEEE-Presentation">
   <a href="https://www.youtube.com/watch?v=rm5pcUggZzs">
<img src="https://img.youtube.com/vi/rm5pcUggZzs/maxresdefault.jpg" width="50%">
      </a>
  </p>

## Trailers
#### Trailer 1
The trailer gives a light on the problem so the audience can start thinking about it.
The trailer captures the audience's mind and the audience will ask themselves....
What is ARGUS?
How will it help to save people's lives?
<p align="center">
   <a href="https://www.youtube.com/watch?v=8GmcOIeVAp4">
<img src="https://img.youtube.com/vi/8GmcOIeVAp4/maxresdefault.jpg" width="50%">
      </a>
  </p>
  

#### Trailer 2 (Main Trailer)
The trailer discusses the problem of road crashes and how argus will help to solve this problem
<p align="center">
  
   <a href="https://www.youtube.com/watch?v=nHsk8bgKjX0">
<img src="https://img.youtube.com/vi/nHsk8bgKjX0/maxresdefault.jpg" width="50%">
      </a>
  </p>


  <h2 id="Demo">
Demo
</h2>

#### Explaination
Explaining in Arabic how to test a video in Argus
<p align="center">
   <a href="https://www.youtube.com/watch?v=92DqypG8TKY">
<img src="https://img.youtube.com/vi/92DqypG8TKY/maxresdefault.jpg" width="50%">
      </a>
  </p>
  
#### Output
The video shows a compilation of road crashes which is the output of the system

<p align="center">
   <a href="https://www.youtube.com/watch?v=R74K5aWLSLk">
<img src="https://img.youtube.com/vi/R74K5aWLSLk/maxresdefault.jpg" width="50%">
      </a>
  </p>




  
