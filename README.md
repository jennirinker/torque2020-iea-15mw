# torque2020-iea-15mw
Files and plotting-code for Torque 2020 paper on IEA 15 MW loads comparison

# Using DVC

The data is now tracked using Data Version Control, my new favorite thing.
Instructions are below.

Install it from [https://dvc.org/](https://dvc.org/). It works from normal
git prompt and is very similar to git. DVC simply creates gitignores and
text files that are tracked using git, but the files themselves are
pushed/pulled from a remote server.

## Configuring the google drive folder as the remote

Once you have been added as a valid user to the Google Drive folder:

```
dvc remote add -d myremote gdrive://1DfIVGMCump70XDN_EB4rzAL2nhgvY6VB
```

The ID is specific to the folder for this Torque paper, and the `-d`
flag sets this as your default.


## Pulling data

```
dvc pull
```

It will pull any changes from the Google Drive.

## Pushing data

Add the added/changed file. E.g. 

```dvc add results/DLC11_v1```

Then, in git, add/commit the text files corresponding to
the data file or directory.

```
git add results/DLC11_v1.dvc
git commit -m "resimulated ElastoDyn with updated parameters"
dvc push
git push origin master
```
