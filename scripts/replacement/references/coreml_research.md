# Core ML export and precision notes

The selected app artifact is fixed-batch224×224 RGB **FP32 EfficientNet-B0**, with151 raw logits and embedded ImageNet normalization. Use the [active model contract](../../../iDex/Recognition/MODEL.md) and [Apple workflow](../apple/README.md), rather than changing architecture/resolution/precision without validation.

Source tensor checkpoints load through the installed TorchVision implementation with tensor-only deserialization and strict label/key checks. The model is set to evaluation mode before tracing. [Apple's image input guide](https://apple.github.io/coremltools/docs-guides/source/image-inputs.html) explains ImageType preprocessing; use global scale1/255 with the exact channelwise normalization embedded once, not an averaged approximation.

Create distinct FP32 and FP16 diagnostic packages. [Typed execution](https://apple.github.io/coremltools/docs-guides/source/typed-execution.html) documents that compute precision affects numerical results. The tested FP32 artifact passed source-reference checks; FP16 and mixed diagnostics had policy-dependent drift or non-finite output. Do not widen tolerances to hide that result or infer a particular compiler bug without a reproducer.

[FP16ComputePrecision op selection](https://apple.github.io/coremltools/source/coremltools.converters.convert.html) can retain sensitive arithmetic in FP32 for a bounded diagnostic. Such a variant still needs the complete fixture set, each intended policy, real-device validation and task-level evaluation. A small passing pilot is not sufficient.

Use `.cpuOnly`, `.cpuAndGPU`, `.cpuAndNeuralEngine`, and `.all` as separate test configurations. They allow backends; they do not prove actual operator placement. Keep Instruments/compute-plan diagnostics separate from unprofiled latency measurements. Core ML's synchronous return and output reading must complete before ending the prediction timer.

Report input preparation, prediction, postprocessing, model loading and encoded-bytes-to-result scope separately. Warm and sustained workloads must use a matched fixture cycle for controlled comparisons, and model/policy order should be counterbalanced. Model reopens share OS/runtime caches; fresh-process and reboot-cold measurements are separate protocols. Simulator results are not phone evidence, and thermal-state labels are not temperature sensors.
