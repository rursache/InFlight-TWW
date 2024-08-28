# InFlight TWW - Taxi-Timer

![InFlight-WW](https://raw.githubusercontent.com/rursache/InFlight-TWW/master/icon.jpg)

The fixed version of the popular InFlight addon for World of Warcraft (Retail)

----

**Download**: [Curseforge](https://legacy.curseforge.com/wow/addons/inflight-tww) | [GitHub](https://github.com/rursache/InFlight-TWW/releases)

----

This fork comes with the following fixes and improvements:
- Added support for 10.2.7, 11.0.0 and 11.0.2
- Added a [python script](https://github.com/rursache/InFlight-TWW/blob/master/merge.py) that merges all the `InFlight.lua` saved values flight path times from the users with the `Default.lua` from the addon.
  - This is the easiest way to have an up to date database for everyone
  - Please contribute by providing your `InFlight.lua` file [here](https://github.com/rursache/InFlight-TWW/issues/1)

![img](https://i.imgur.com/6yKOruq.png)

Developed initially by: [totalpackage](https://www.wowinterface.com/forums/member.php?action=getinfo&userid=27891), [R_X](https://www.wowinterface.com/forums/member.php?action=getinfo&userid=341594), [Uitat](https://www.wowinterface.com/forums/member.php?action=getinfo&userid=272556)

## Description
InFlight is a simple taxi flight timer mod that lets you know how long it will take to get to your destination. Other mods may provide a similar feature, however, InFlight is a lightweight alternative that, in most cases, is leaner, faster and uses a lot less memory (which is the main motivation behind InFlight).

## Features:
- Take-off confirmation
- Many customization options for the look of the timer bar
- Support for Druid-only and some other special flight paths
- Already has most flight times
- Learns new flight times or updates existing flight times when taxis are used
- Flight times added to tooltip on flight map

## How to Use:
InFlight is LoadOnDemand to use less memory when not needed
'/inflight', right-click on the timer bar, or check interface options to customize
Shift left-click and drag to move the timer bar
