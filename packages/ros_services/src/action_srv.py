#!/usr/bin/env python3

from example_service.srv import Fibonacci, FibonacciResponse  # imports the service types
import rospy

# Brings in the SimpleActionClient
import actionlib

# inside Fibonacci.srv/Fibonacci:
# uint64 order -- this is the request
# ---
# uint64[] sequence  -- this is the result

################## making a service available in your node

def handle_fib(req):
    rospy.loginfo("Returning: %s", str(req.order))  # is the function to handle the callback when service is called
    return FibonacciResponse(req.order)


def action_srv():
    rospy.init_node('action_srv')
    # rospy.init_node('add_two_ints_server')
    s = rospy.Service('action_srv', Fibonacci, handle_fib)  # declares a new service named "hw9_fib_server" with type 'Fibonacci' -- similar to subscriber
    rospy.loginfo("Ready to output fibonacci numbers")
    rospy.spin()


##################

################## calling a service in your node/ writing the client node

# running /rosservice call /calc_fibonacci 3 is not working?

def add_two_ints_client(x):
    rospy.wait_for_service('action_srv')  # waits for service to become available
    try:
        action_srv = rospy.ServiceProxy('calc_fibonacci', Fibonacci)  # setup the service -- similar to subscribing to calc_fibonacci?
        resp1 = action_srv(x)  # requests the service
        return resp1.sequence
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

##################

if __name__ == "__main__":
    action_srv()
    add_two_ints_client(3)
    rospy.spin()
