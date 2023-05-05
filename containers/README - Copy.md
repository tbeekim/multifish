# Docker Containers

This directory contains one subfolder for every Docker container used in the pipeline. Each container packages the entire system environment necessary for running that step of the pipeline, making the pipeline trivially portable across sytems.

To easily rebuild these containers, install Docker and [maru](https://github.com/JaneliaSciComp/maru) and run `maru build`. 

See the [Development docs](../docs/Development.md) for more information.

## changed starfinity_prediction file from :

label_starfinity, res_dict = model.predict_instances(img_normed,
                                                         n_tiles=n_tiles,
                                                         affinity=True,
                                                         affinity_thresh=0.1,
                                                         verbose=True)


to:

label_starfinity, res_dict = model.predict_instances_big(img_normed, block_size=(512,1024,1024),min_overlap=(96,96,96), affinity=True, affinity_thresh=0.1, n_tiles=n_tiles, candidate_grid=2, verbose=True)

