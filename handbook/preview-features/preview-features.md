# Preview Features

This section contains guided help for preview features in the current SystemLink release. While preview features are not yet complete and have limited functionality, they provide an understanding of the direction the product is taking and give users the opportunity to experiment and give feedback.

## Creating and Uploading Analysis Automation Procedures with Jupyter Notebooks

Analysis Automation performs recurring analyses with similar data and exports the results as a PDF or graphics file for management reporting. Analysis automation procedures define the analyses and contain the analysis script, the parameter definition, and the search query for the respective data. Currently, you create procedures in DIAdem VBS or Python, but now you can also create them in Jupyter and upload them straight to Analyis Automation.  

### Prerequisites

To create analysis automation procedures with Jupyter in SystemLink, you need to install SystemLink 2021 R1 and the Measurement Data Analysis and Jupyter Hub modules.

### Steps to Take

Create an analysis automation procedure from the analysis notebook you write in Jupyter and upload it to the procedures library in Analysis Automation.

1. In __Jupyter__, open the analysis notebook you want to upload.

2. Right-click the notebook and select __New Analysis Automation Procedure__.

<figure>
  <img src="../../img/new_aa_procedure.png" width="500" />
  <figcaption>Create a new analysis automation procedure from the notebook.</figcaption>
</figure>

1. In the dialog box, specify the following information:
    1. Enter a name and description for the procedure.
    2. Choose a __Workspace__ to define the users and the available data sources that can interact with the procedure.
    3. In the dropdown menu, choose a __Search Query__ you saved in Data Navigation.
      The query defines the data you want to analyze with the analysis notebook. Verify that the data sources in the query are in the workspace you chose.
    4. Select the __Execution Mode__.
      Select __Compare__ if you want to run the analysis notebook on all data elements the search query retrieves.
      Select __Parallel__ if you want to run the analysis notebook on each data element the search query retrieves.
2. Click __OK__.
    The procedure uploads to Analysis Automation.
3. Click the __Analysis Automation__ link to view the procedure on the __Procedures__ tab in Analysis Automation.
4. Approve the procedure for it to go live.  
*Note: Approving procedures requires the __Approve and reject procedures__ privilege.*

After uploading the procedure, [add a task to execute your procedure in Analysis Automation](https://www.ni.com/r/slmanual/analysis/adding-editing-tasks-for-analysis-automation-procedures/).
