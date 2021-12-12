# NLB IP Updater

Helper util for populating a NLB target group with IP addresses of a ALB. https://aws.amazon.com/blogs/networking-and-content-delivery/using-static-ip-addresses-for-application-load-balancers/

## FGP changes: 
We have made following modifications to they python code [Common.py](populate_NLB_TG_with_ALB/common.py) in order for it to make it work: 

1. commented out line 52 where do disable the default resolver machanism. When this line is enabled this nslookup does not work. 
2. line 266 the default mechanism is if in the environment variables it detects SAME_VPC it will try to update the listener with out all availability zones. I just made both coditions the same. 