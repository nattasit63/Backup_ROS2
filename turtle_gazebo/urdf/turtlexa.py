<?xml version="1.0"?>
<robot name= "robot_description" xmlns:xacro="http://www.ros.org.wiki/xacro">
 	<xacro:include filename="$(find turtle_description)/urdf/turtle_properties.xacro"/> 
 	<xacro:include filename="$(find turtle_description)/urdf/turtle_chassis.xacro"/> 
 	<xacro:include filename="$(find turtle_description)/urdf/turtle_wheel.xacro"/> 
 	<xacro:include filename="$(find turtle_description)/urdf/turtle_castor.xacro"/>
	<xacro:chassis
	 	parent="base_footprint" child= "base_link"/>
 	<xacro:wheel 
 		name="left"
 		translation="
 			0 
 			${WHEEL_SEPARATION/2}
 			${WHEEL_RADIUS-(BASE_HEIGHT/2 +BASE_ELEVATION)}"
 		rotation="0 0 0"
 		parent="base_link"/> 
 	<xacro:wheel 
 		name="right"
 		translation="
 			0 
 			${-WHEEL_SEPARATION/2} 
 			${WHEEL_RADIUS-(BASE_HEIGHT/2+BASE_ELEVATION)}"
 		rotation="0 0 0"
 		parent="base_link"/> 

 	<xacro:castor
 		name="right_front"
 		translation="
 			${CASTOR_SEPARATION_X/2} 
 			${CASTOR_SEPARATION_Y/2} 
 			${CASTOR_RADIUS-(BASE_HEIGHT/2+BASE_ELEVATION)}"
 		rotation="0 0 0"
 		parent="base_link"/> 


 	<xacro:castor 
 		name="left_front"
 		translation="
 			${CASTOR_SEPARATION_X/2} 
 			${-CASTOR_SEPARATION_Y/2} 
 			${CASTOR_RADIUS-(BASE_HEIGHT/2+BASE_ELEVATION)}"
 		rotation="0 0 0"
 		parent="base_link"/> 
 	<xacro:castor 
 		name="right_rear"
 		translation="
 			${-CASTOR_SEPARATION_X/2} 
 			${CASTOR_SEPARATION_Y/2} 
 			${CASTOR_RADIUS-(BASE_HEIGHT/2+BASE_ELEVATION)}"
 		rotation="0 0 0"
 		parent="base_link"/> 
 	<xacro:castor 
 		name="left_rear"
 		translation="
 			${-CASTOR_SEPARATION_X/2} 
 			${-CASTOR_SEPARATION_Y/2} 
 			${CASTOR_RADIUS-(BASE_HEIGHT/2+BASE_ELEVATION)}"
 		rotation="0 0 0"
 		parent="base_link"/>
</robot>


 