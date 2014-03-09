Shape Fuse
======================
This python script for Silhouette will create a curve based on other curves animated points

If you like it, use it frequently, or want to support further development please consider a small donation to the author.   
<a href='http://www.pledgie.com/campaigns/21123'><img alt='Click here to lend your support to: VFX tools coding project and make a donation at www.pledgie.com !' src='http://www.pledgie.com/campaigns/21123.png?skin_name=chrome' border='0' /></a>

#### Compatibility ####
Silhouette 5.1.2 and up (not tested on previous versions)

#### KNOW LIMITATIONS #####
 Creates only B-spline shapes for now

#### USAGE ####
1. Place both .py files inside your actions folder (osx:/Applications/SilhouetteFX/Silhouette5.1.2/Silhouette.app/Contents/Resources/scripts/)
2. This script should be used with keyboard shortcuts, create/add then in your Silhouette sfxuser.py:
```
import fx
def callMethod(func, *args, **kwargs):
    def _return_func():
        return func(*args, **kwargs)
    return _return_func

fx.bind('shift+F12', callMethod(fx.actions["bvfx_ShapeFuse"].execute,"build"))
fx.bind('F12', callMethod(fx.actions["bvfx_ShapeFuse"].execute,"collect"))
```
3. Collect shape points one by one (F12 on the example above), when point collection is done, use the Build shortcut (shift+F12 on the example above).
 
#### Licensing ####
This script is made available under a BSD Style license that is included in the package.
