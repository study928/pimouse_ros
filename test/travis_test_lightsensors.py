#!/usr/bin/env python
#encording: utf8
import rospy, unittest, rostest
import rosnode
import time
from pimouse_ros.msg import LightSensorValues

class LightsensorTest(unittest.TestCase):
	def set_up(self):
		self.count = 0
		rospy.Subscriber('/lightsensors', LightSensorValues, self.callback)
		self.values = LightSensorValues()

	def callback(self, data):
		self.count += 1
		self.values = data

	def check_values(self, lf, ls, rs, rf):
		vs = self.values
		self.assertEqual(vs.left_forward, lf, 'defferent values: left_forward')
                self.assertEqual(vs.left_side, ls, 'defferent values: left_side')
                self.assertEqual(vs.right_side, rs, 'defferent values: right_side')
                self.assertEqual(vs.right_forward, rf, 'defferent values: right_forward')
                self.assertEqual(vs.sum_all, lf+ls+rs+rf, 'defferent values: sum_all')
                self.assertEqual(vs.sum_forward, lf+rf, 'defferent values: sum_forward')

	def test_node_exist(self):
		nodes = rosnode.get_node_names()
		self.assertIn('/lightsensors', nodes, "node does not exist")

	def test_get_values(self):
		rospy.set_param('lightsensors_freq', 10)
		time.sleep(2)

		with open("/dev/rtlightsensors0", "w") as f:
			f.write('-1 0 123 4321\n'

		time.sleep(3)
		
		self.assertFalse(self.count == 0, 'cannot subscribe the topic')
		self.check_valuse(4231, 123, 0, -1)
	def test_change_parameter(self):
		rospy.set_param('lightsensors_freq', 10)
		time.sleep(2)
		c_prev = self.count
		time.sleep(3)
		
		self.assertTrue(self.count < c_prev + 4, 'freq does not change')
		self.assertFalse(self.count == c_prev, 'sbuscriber is stopped')

if __name__ == '__main__':
	time.sleep(3)
	rospy.init_node('travis_test_lightsensors')
	rostest.rosrun('pimouse_ros', 'travis_test_lightsensors.py', LightsensorTest)

