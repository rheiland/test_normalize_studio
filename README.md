# test_normalize_studio

Studio GUI to experiment with motility and chemotaxis

Compile the C++ model:
```
cd src
make

# move the executable to where the Studio wants it:
mv myproj ..

# Change directory to the root dir and run the GUI from there
cd ..
python bin/studio.py
```

In the GUI:
* in the Run tab, click `Run Simulation`. Note: the simulation is run *from* the `tmpdir` directory and that's where all output files will be written.
* in the Plot tab, click `Play`.
* edit params if you want then repeat: Run, Play.

Test cases:
* look at what's being printed as terminal output in the Run tab 
* in Cell Types | Motility: uncheck "enable motility" and re-run, plot
* in Cell Types | Motility: check "enabled" on Chemotaxis and re-run, plot
* in Cell Types | Motility: check "enable motility", check "enabled" on Chemotaxis and re-run, plot (with "Substrates" checked)