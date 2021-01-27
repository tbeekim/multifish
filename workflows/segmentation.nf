include {
    predict;
} from '../processes/segmentation'  addParams(lsf_opts: params.lsf_opts,
                                              segmentation_container: params.segmentation_container)

workflow segmentation {
    take:
    segmentation_inputs

    main:

    segmentation_inputs \
    | map { args ->
        [
            args.data_dir,
            args.dapi_channel,
            args.scale,
            args.model_dir,
            "${args.segmentation_output_dir}/${args.acq_name}-${args.dapi_channel}.tif"
        ]
    } \
    | predict \
    | set { done }

    emit:
    done
}