# 3D-Tank-Implementation-with-Pygame
Implement a simple 3D tank shooting game using the OpenGL and/or the GLU library with the following components:
The battlefield: The battlefield is to be drawn on the X-Y plane. It has a dimension of 300 x 300 units (width x height) and it must be flat (i.e. no terrain elevation, etc.).

The battlefield is to be divided into three parts; (1) part A where the player tank can move on, (2) part B where the target vehicle moves on and (3) the river that separates part A and part B from each other. The top view of the battlefield with dimensions to be used for the implemented.

part A occupies the lower half of the total battlefield area. Then the river with the uniform width of 20 units is placed next to part A and the rest of the area is part B.
All three parts of the battlefield (part A, part B and the river) must be mapped with texture to give a realistic look to the game. 

The player’s tank: The player’s tank is to be drawn in 3D. The body of the tank must be drawn with a minimum of three parts; 
(1) tank body, 
(2) tank cannon and 
(3) the tank’s wheels. 
The tank's body can be modeled as any proper shape but the dimension is limited to 10 x 10 x 10 units (length x width x height). The cannon is to be drawn using a proper shape (e.g. cylinder) but the cannon's length is limited to 10 units. The cannon has its starting point at the center of the tank body where the starting point also acts as a rotating point of the cannon. The cannon is also tilted
according to the cannon's angle given by the user input. The tank's wheels must rotate while the tank is moving.
The player tank must be drawn at least by using filled polygon objects with assigned material properties (e.g. diffuse, ambient and specular colors). Texture mapping on the tank's part is allowed but is not required. The tank is to be driven only on part A of the battlefield (it must not cross the river).

The cannon ball: the player tank can shoot cannon balls. The 3D shooting projectile will be provided by the game engine. The cannon balls has drawn in 3D. The cannon balls drawn at least by using filled polygon objects with assigned emission color to the material property to make it look like it is glowing. Also, a positional light source must be placed at the center location of the cannon ball to emit light that lights up nearby objects in the scene.

The explosion: the explosion takes place at the location where the cannon ball hits the battlefield. The explosion has to be drawn in 3D. The explosion must be drawn at least by using a gluSphere in order to give the user a visual feedback of the shooting result. Optionally, the size of the explosion sphere should become larger after it hits the battle field.

The target vehicle: a target vehicle is to be drawn in 3D. The body of the vehicle must be drawn with a minimum of two parts; (1) vehicle body and 
(2) wheels. 
The vehicle's body can be modeled as any proper shape but the dimension is limited to 15 x 15 x 15 unit (length x width x height). The vehicle's wheels must rotate while the vehicle is moving.
The target vehicle has drawn at least by using filled polygon objects with assigned material properties (e.g. diffuse, ambient and specular colors). The material color of the target vehicle must be changed each time the target vehicle is being hit by the cannon ball. The vehicle is to be driven on the X-Y plane in ellipse course (refer to the yellow ellipse in Figure 2) given by the game engine.

A big building: a building is to be drawn in 3D using OpenGL library. The building has drawn with a minimum of four walls. The maximum size of the building is limited to 50 x 50 x 50 units (width x length x height). The building must be mapped with texture in order to make it look like a real building. The building must be placed at the center of part B of the battlefield.

Lighting: It has one directional light source must be provided in order to light up the objects in the scene.

Camera setup: the camera has set in perspective mode (that is, using perspective projection and NOT the orthographic projection). The user should be able to change the camera setup using the keys "1, 2, 3 and 4" on the keyboard. At least four camera setup described below has to be provided:
o Behind the player’s tank and always looking ahead (key "1"): this camera’s "eye position" is located somewhere behind the player’s tank and it follows the movement of the tank by maintaining constant distance and orientation towards the player’s tank. The camera always looks ahead towards the driving direction of the player’s tank.
o Near the target vehicle and looking at the player’s tank (key "2"): this camera’s "eye position" is located near the target vehicle in a way that the target vehicle can always be seen. The "look at" position is the position of the player’s tank.
o Above the building, looking at the target vehicle (key "3"): this camera’s "eye position" is located above the building and the "look at" position is the position of the target tank.
o Above the building, looking at the cannon ball (key "4"): this camera setup is a special mode that should only be activated during the shooting process. That is, when key "4" is pressed the current camera setup (one of the three mode mentioned above) is still being used. Only when the cannon ball status "shooting" is True (cannon ball flying in the air) then this camera setup has to be enabled so that the user sees the flying cannon ball. Once the cannon ball status "shooting" is False (cannon ball hits the battlefield), the camera setup has to change back to the camera setup previously assigned by the user (one of the three above).

In this setup, the camera’s "eye position" is located above the building and the "look at" position is the position of the cannon ball. Game play:
1. Initialize the scene with a battlefield and all its components.
2. Update the position and orientation of the target vehicle according to the game engine variables.
3. Let the user drive the player tank around part A of the battlefield by using the arrow keys on the keyboard to drive the tank forward/backward and rotate clockwise/counter-clockwise. (Hint: using the point-to-point distance function
to check the distance between the center of the tank and the river to limit the movement of the tank to part A of the battlefield).
4. Let the user adjust the angle of the cannon using the key 'A' for tilting the cannon up and the key 'Z' to tilt the cannon down. The angle of the cannon is to be limited to the range of 15-85 degrees.
5. Let the user shoot the cannon ball by hitting the ENTER key.
6. The cannon ball should appear traveling according to the calculated projectile given by the game engine until it hits the battlefield surface. An explosion has to take place at the position where the cannon ball hits the battlefield.
7. For each frame, check if the cannon ball hit the target (Hint: using the point-to-point distance function to check the distance between the center of the cannon ball and the target).
a. If the target is hit, change the material color of the target vehicle, start over at step (2).
b. If the target is not hit, repeat at step (3).
