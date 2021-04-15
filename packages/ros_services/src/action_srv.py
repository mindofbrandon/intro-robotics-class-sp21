#!/usr/bin/env python3

from Fibonacci.srv import uint64    # imports the service types
import rospy


################## making a service available in your node
def handle_add_two_ints(req):
    print("Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b)))   # is the function to handle the callback when service is called
    return AddTwoIntsResponse(req.a + req.b)

def add_two_ints_server():
    rospy.init_node('action_srv')
    # rospy.init_node('add_two_tints_server')
    s = rospy.Service('add_two_ints', AddTwoInts, handle_add_two_ints)  # advertises the service and maps it to the callback
    # print("Ready to add two ints.")
    # rospy.spin()
##################

################## calling a service in your node

def add_two_ints_client(x, y):
    rospy.wait_for_service('add_two_ints')  # waits for service to become available
    try:
        add_two_ints = rospy.ServiceProxy('add_two_ints', AddTwoInts)   # setup the service
        resp1 = add_two_ints(x, y)  # requests the service
        return resp1.sum
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)


##################




if __name__ == "__main__":
    add_two_ints_server()
    add_two_ints_client(1,2)
    rospy.spin()