#### 6/16/26
Should threshold value depend on k? Right now it is dependent on a scale factor of the average of the means. Heres why:
At the point where threshold is relevant, Bob receives E which is basically S/n + sum(k)/n or S/n + sum(k)/n - mu where mu is the opposite 

ToDo for Wednesday, 6/24 at 8:30 NYC time

- Implement max/min protocol. Remember that max/min are different protocols, one where Bob always selects the minimum from his trials and one where bob selects the maximum from his trials. 
    - See which one provides a better success rate
- If the above fails, consider switching protocol to a different distribution (beta, burr, etc.)
- Create several graphs to visualize change in success rate as one parameter changes. 
- Organize repository and update readme 
    - Create two folders, "testing" and "For Prof. Shpilrain" to delineate between files in flux and files ready for testing by professor

Time allowing, think more critically about how the information in bob's set travels through the protocol, and similarly how the threshold operates in separating success from failure.
Also consider how false positives and negatives may occur 