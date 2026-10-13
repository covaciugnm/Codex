# Rezultate — Enumeră nodurile implicite ale cam

Răspunsuri și rezultate disponibile în istoricul local; fără limită de lungime aplicată de export.

## Asistent

Voi verifica modelul OAK-D-Pro AF din fotografie și codul aplicației, ca să separ nodurile pornite implicit de cele disponibile pentru activare ulterioară.


## commandExecution

````json
{
  "type": "commandExecution",
  "id": "exec-44a8f1a8-2f65-4112-a2ee-90557af58acf",
  "pluginId": null,
  "scriptPath": null,
  "command": "\"C:\\\\Users\\\\User\\\\.cache\\\\codex-runtimes\\\\codex-primary-runtime\\\\dependencies\\\\native\\\\powershell\\\\pwsh.exe\" -Command 'Get-ChildItem -Force | Select-Object Name,Mode'",
  "cwd": "S:\\3dscan.eva-org.com",
  "processId": null,
  "source": "unifiedExecStartup",
  "status": "failed",
  "commandActions": [
    {
      "type": "unknown",
      "command": "Get-ChildItem -Force | Select-Object Name,Mode"
    }
  ],
  "aggregatedOutput": "Failed to create unified exec process: CreateProcessWithLogonW failed: 267",
  "exitCode": -1,
  "durationMs": 0
}
````

## commandExecution

````json
{
  "type": "commandExecution",
  "id": "exec-47699c57-cfc0-43c0-bef6-06c8e7a6a7aa",
  "pluginId": null,
  "scriptPath": null,
  "command": "\"C:\\\\Users\\\\User\\\\.cache\\\\codex-runtimes\\\\codex-primary-runtime\\\\dependencies\\\\native\\\\powershell\\\\pwsh.exe\" -Command \"Get-ChildItem -LiteralPath 'S:\\\\3dscan.eva-org.com' -Force | Select-Object Name,Mode\"",
  "cwd": "C:\\Users\\User",
  "processId": "85743",
  "source": "unifiedExecStartup",
  "status": "failed",
  "commandActions": [
    {
      "type": "unknown",
      "command": "Get-ChildItem -LiteralPath 'S:\\3dscan.eva-org.com' -Force | Select-Object Name,Mode"
    }
  ],
  "aggregatedOutput": "Get-ChildItem: \r\nLine |\r\n   2 |  Get-ChildItem -LiteralPath 'S:\\3dscan.eva-org.com' -Force | Select-Ob …\r\n     |  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\r\n     | Cannot find drive. A drive with the name 'S' does not exist.\r\n",
  "exitCode": 1,
  "durationMs": 426
}
````

## webSearch

````json
{
  "type": "webSearch",
  "id": "exec-8a053374-7c26-428e-91df-35a82d4eeb07",
  "query": "site:docs.luxonis.com OAK D Pro RVC2 pipeline nodes boot firmware ...",
  "action": {
    "type": "search",
    "query": null,
    "queries": [
      "site:docs.luxonis.com OAK D Pro RVC2 pipeline nodes boot firmware",
      "site:docs.luxonis.com software depthai nodes RVC2"
    ]
  },
  "results": [
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn0search0",
      "snippet": "Supported on:RVC2 RVC4 ... 2 replay = pipeline.create(dai.node.ReplayVideo)` ... `std::filesystem::path getReplayMetadataFile()`",
      "title": "ReplayVideo",
      "url": "https://docs.luxonis.com/software-v3/depthai/depthai-components/host_nodes/replay_video"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn0search1",
      "snippet": "You can use .blob, superblob, or NNArchive formats, and target various platforms (RVC2, RVC3, RVC4). ... * DepthAI Model Zoo ... 6 nn = dai.node.NeuralNetwork.build(tensor_input,",
      "title": "NeuralNetwork",
      "url": "https://docs.luxonis.com/software-v3/depthai/depthai-components/nodes/neural_network"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn0search2",
      "snippet": "Host nodes are implemented using the `HostNode` and `ThreadedHostNode` classes, which provide a framework for creating custom host-side logic within the pipeline.DepthAI comes with several",
      "title": "Host Nodes",
      "url": "https://docs.luxonis.com/software-v3/depthai/depthai-components/host_nodes"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn0search3",
      "snippet": "The depthai module is implicitly imported to the script node. ... RVC2 RVC4",
      "title": "Script",
      "url": "https://docs.luxonis.com/software-v3/depthai/depthai-components/nodes/script"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn0search4",
      "snippet": "Supported on:RVC2 RVC4 ... 2#include <depthai/pipeline/node/host/RGBD.hpp>",
      "title": "RGBD",
      "url": "https://docs.luxonis.com/software-v3/depthai/depthai-components/nodes/rgbd"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn0search5",
      "snippet": "* DepthAI v3 ToF architecture ... Supported on:RVC2The `ToF` node converts raw Time-of-Flight sensor data into depth and exposes both base and filtered outputs.",
      "title": "ToF",
      "url": "https://docs.luxonis.com/software-v3/depthai/depthai-components/nodes/tof"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn0search6",
      "snippet": "Supported on:RVC2 RVC4 ... Added in DepthAI v3.6.0. ... By default the node reads `T_frame_to_ref` from the depth frame's `ImgTransformation` extrinsics and applies it, so",
      "title": "PointCloud",
      "url": "https://docs.luxonis.com/software-v3/depthai/depthai-components/host_nodes/pointcloud"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn0search7",
      "snippet": "* 4 TOPS of processing power (1.4 TOPS for AI) - RVC2 NN Performance ... * Stereo pipeline - Stereo matching (census transform, cost matching",
      "title": "Robotics Vision Core 2",
      "url": "https://docs.luxonis.com/hardware/platform/rvc/rvc2"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn0search8",
      "snippet": "Each node provides a specific functionality on the DepthAI, a set of configurable properties and inputs/outputs.After you create a node on a pipeline, you can",
      "title": "Device Nodes",
      "url": "https://docs.luxonis.com/software-v3/depthai/depthai-components/nodes"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn0search9",
      "snippet": "Supported on:RVC2 RVC4 ... Warp node is also run on Warp engine (HW block on RVC4 chip).",
      "title": "Warp",
      "url": "https://docs.luxonis.com/software-v3/depthai/depthai-components/nodes/warp/"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn0search10",
      "snippet": "DepthAI `3.7.1` adds a GPU backend for `ImageManip` on RVC4. ... 2 manip.setBackend(dai.node.ImageManip.Backend.GPU)`",
      "title": "ImageManip",
      "url": "https://docs.luxonis.com/software-v3/depthai/depthai-components/nodes/image_manip"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn0search11",
      "snippet": "Supported on:RVC2 ... Image This example requires the DepthAI v3 API, see installation instructions. ... 10 camRgb = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_A)",
      "title": "Edge Detector",
      "url": "https://docs.luxonis.com/software-v3/depthai/examples/rvc2/edge_detector/edge_detector"
    }
  ]
}
````

## commandExecution

````json
{
  "type": "commandExecution",
  "id": "exec-cc7a4794-c4d2-4be4-898e-6f3369e1f696",
  "pluginId": null,
  "scriptPath": null,
  "command": "\"C:\\\\Users\\\\User\\\\.cache\\\\codex-runtimes\\\\codex-primary-runtime\\\\dependencies\\\\native\\\\powershell\\\\pwsh.exe\" -Command \"Get-ChildItem -LiteralPath 'S:\\\\3dscan.eva-org.com' -Force | Select-Object Name,Mode\"",
  "cwd": "C:\\Users\\User",
  "processId": "32079",
  "source": "unifiedExecStartup",
  "status": "failed",
  "commandActions": [
    {
      "type": "unknown",
      "command": "Get-ChildItem -LiteralPath 'S:\\3dscan.eva-org.com' -Force | Select-Object Name,Mode"
    }
  ],
  "aggregatedOutput": "Get-ChildItem: \r\nLine |\r\n   2 |  Get-ChildItem -LiteralPath 'S:\\3dscan.eva-org.com' -Force | Select-Ob …\r\n     |  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\r\n     | Cannot find drive. A drive with the name 'S' does not exist.\r\n",
  "exitCode": 1,
  "durationMs": 319
}
````

## webSearch

````json
{
  "type": "webSearch",
  "id": "exec-5a40f85a-362a-4d10-a49b-3fbd4d903721",
  "query": "https://docs.luxonis.com/software/depthai-components/nodes/",
  "action": {
    "type": "openPage",
    "url": "https://docs.luxonis.com/software/depthai-components/nodes/"
  },
  "results": [
    {
      "type": "text_result",
      "ref_id": "turn1view0",
      "snippet": "Total lines: 1",
      "title": "Internal Error"
    },
    {
      "type": "text_result",
      "ref_id": "turn1view1",
      "snippet": "Total lines: 1",
      "title": "Internal Error"
    },
    {
      "type": "text_result",
      "ref_id": "turn1view2",
      "snippet": "Total lines: 1",
      "title": "Internal Error"
    }
  ]
}
````

## Asistent

Documentația confirmă că nodurile de procesare sunt definite de pipeline-ul aplicației; modelul camerei nu stabilește singur ce rulează. Unitatea S: nu este accesibilă în această sesiune, așa că nu pot confirma încă lista activată de aplicația voastră. Voi distinge această limită de capabilitățile camerei.


## webSearch

````json
{
  "type": "webSearch",
  "id": "exec-4351e3a9-8c9e-44f1-8194-54fa11642f91",
  "query": "site:docs.luxonis.com \"Device\" \"firmware\" \"pipeline\" \"uploaded\" ...",
  "action": {
    "type": "search",
    "query": null,
    "queries": [
      "site:docs.luxonis.com \"Device\" \"firmware\" \"pipeline\" \"uploaded\"",
      "site:docs.luxonis.com \"Nodes\" \"AprilTag\" \"SPIOut\" \"PointCloud\"",
      "site:docs.luxonis.com \"OAK-D Pro\" \"disabled\" \"IR\"",
      "site:docs.luxonis.com \"OAK-D Pro\" \"BMI270\""
    ]
  },
  "results": [
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn2search0",
      "snippet": "# OAK-D Pro ... The Pro version of this device has notch IR filters at 940nm on the stereo camera pair, which allows both visible",
      "title": "OAK-D Pro",
      "url": "https://docs.luxonis.com/hardware/products/OAK-D%20Pro"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn2search1",
      "snippet": "When starting the device, you have to upload a Pipeline to it, which will get executed on the VPU.When you create the device in the",
      "title": "Device",
      "url": "https://docs.luxonis.com/software-v3/ai-inference/conversion/rvc-conversion/offline/"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn2search2",
      "snippet": "# OAK-D Pro W ... The Pro version of this device has notch IR filters at 940nm on the stereo camera pair, which allows both",
      "title": "OAK-D Pro W",
      "url": "https://docs.luxonis.com/hardware/products/OAK-D%20Pro%20W"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn2search3",
      "snippet": "# OAK-D Pro W PoE ... The Pro version of this device has notch IR filters at 940nm on the stereo camera pair, which allows",
      "title": "OAK-D Pro W PoE",
      "url": "https://docs.luxonis.com/hardware/products/OAK-D%20Pro%20W%20PoE"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn2search4",
      "snippet": "# OAK 4 D Pro ... The Pro version of this device has notch IR filters at 940nm on the stereo camera pair, which allows",
      "title": "OAK 4 D Pro",
      "url": "https://docs.luxonis.com/hardware/products/OAK%204%20D%20Pro"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn2search5",
      "snippet": "Due to supply chain issues, most of the OAK camera that were manufactured between Q2 2021 and Q2 2023 have integrated BMI270 - 6-axis IMU",
      "title": "OAK-D W",
      "url": "https://docs.luxonis.com/hardware/products/OAK-D%20W"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn2search6",
      "snippet": "Due to supply chain issues, most of the OAK camera that were manufactured between Q2 2021 and Q2 2023 have integrated BMI270 - 6-axis IMU",
      "title": "OAK-D W PoE",
      "url": "https://docs.luxonis.com/hardware/products/OAK-D%20W%20PoE"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn2search7",
      "snippet": "3 | Eth MX1+ | USB D+ | USB 2.0 interface that can be used to connect to the OAK device (eg. reflash) if USB",
      "title": "OAK-D Pro PoE",
      "url": "https://docs.luxonis.com/hardware/products/OAK-D%20Pro%20PoE"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn2search8",
      "snippet": "Derived by dai::DeviceNodeCRTP< DeviceNode, ToFDepthConfidenceFilter, ToFDepthConfidenceFilterProperties >, dai::DeviceNodeCRTP< DeviceNode, Rectification, RectificationProperties >, dai::DeviceNodeCR",
      "title": "C++ API",
      "url": "https://docs.luxonis.com/software-v3/depthai/api/cpp"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn2search9",
      "snippet": "AprilTag node. ... depthai.node.SPIOut(depthai.DeviceNode)",
      "title": "Python API",
      "url": "https://docs.luxonis.com/software-v3/depthai/api/python"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn2search10",
      "snippet": "Support for host nodes: DepthAI v3 now supports custom host nodes, allowing you to run parts of your pipeline on the host with custom logic",
      "title": "Release Notes",
      "url": "https://docs.luxonis.com/software-v3/depthai/release-notes"
    }
  ]
}
````

## commandExecution

````json
{
  "type": "commandExecution",
  "id": "exec-029a6c47-e7f3-4652-9cba-dfdc7afeb58f",
  "pluginId": null,
  "scriptPath": null,
  "command": "\"C:\\\\Users\\\\User\\\\.cache\\\\codex-runtimes\\\\codex-primary-runtime\\\\dependencies\\\\native\\\\powershell\\\\pwsh.exe\" -Command 'Get-SmbMapping | Select-Object LocalPath,RemotePath,Status'",
  "cwd": "C:\\Users\\User",
  "processId": "87784",
  "source": "unifiedExecStartup",
  "status": "failed",
  "commandActions": [
    {
      "type": "unknown",
      "command": "Get-SmbMapping | Select-Object LocalPath,RemotePath,Status"
    }
  ],
  "aggregatedOutput": "Get-SmbMapping: \r\nLine |\r\n   2 |  Get-SmbMapping | Select-Object LocalPath,RemotePath,Status\r\n     |  ~~~~~~~~~~~~~~\r\n     | Access to a CIM resource was not available to the client.\r\n",
  "exitCode": 1,
  "durationMs": 1258
}
````

## webSearch

````json
{
  "type": "webSearch",
  "id": "exec-0fcf2fe1-8aec-423e-97c0-fc6bf3714aee",
  "query": "site:docs.luxonis.com/software/depthai-components/nodes \"PointCloud\" ...",
  "action": {
    "type": "search",
    "query": null,
    "queries": [
      "site:docs.luxonis.com/software/depthai-components/nodes \"PointCloud\"",
      "site:docs.luxonis.com/software-v3/depthai/depthai-components/nodes \"AprilTag\" \"RVC2\"",
      "site:docs.luxonis.com/software/depthai-components/nodes \"DetectionNetwork\" \"SpatialDetectionNetwork\"",
      "site:docs.luxonis.com \"pipeline\" \"cannot\" \"running\" \"nodes\""
    ]
  },
  "results": [
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn3search0",
      "snippet": "On the RVC2 devices, the AprilTag node runs on the host computer, so the performance will be limited by the host CPU.",
      "title": "AprilTag",
      "url": "https://docs.luxonis.com/software-v3/depthai/depthai-components/nodes/april_tag"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn3search1",
      "snippet": "The pipeline of the SpatialDetectionNetwork node is described in the schema below:Image Spatial Detection node is essentially just an abstraction of the Detection Network (DetectionNetwork",
      "title": "SpatialDetectionNetwork",
      "url": "https://docs.luxonis.com/software-v3/depthai/depthai-components/nodes/spatial_detection_network/"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn3search2",
      "snippet": "By default the node reads `T_frame_to_ref` from the depth frame's `ImgTransformation` extrinsics and applies it, so the output point cloud is in the reference (origin)",
      "title": "PointCloud",
      "url": "https://docs.luxonis.com/software-v3/depthai/depthai-components/host_nodes/pointcloud"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn3search3",
      "snippet": "6 spatialDetectionNetwork = p.create(dai.node.SpatialDetectionNetwork).build(camRgb, stereo, modelDescription, fps=FPS) ... 10 spatialDetectionNetwork.setDepthLowerThreshold(100) ... Luxonis - Robotic",
      "title": "SpatialDetectionNetwork",
      "url": "https://docs.luxonis.com/software-v3/depthai/depthai-components/nodes/spatial_detection_network"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn3search4",
      "snippet": "Minimal example that creates a colorized point cloud from stereo depth and an aligned RGB camera using the PointCloud node.",
      "title": "PointCloud",
      "url": "https://docs.luxonis.com/software-v3/depthai/examples/pointcloud/point_cloud"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn3search5",
      "snippet": "`PointCloudConfig` carries configuration for the PointCloud node. ... ` DEPTHAI_SERIALIZE(PointCloudConfig, Buffer::sequenceNum, Buffer::ts, Buffer::tsDevice, organized, transformationMatrix, lengthUn",
      "title": "PointCloudConfig",
      "url": "https://docs.luxonis.com/software-v3/depthai/depthai-components/messages/pointcloud_config"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn3search6",
      "snippet": "Supported on:RVC2 RVC4Utilizes the AprilTag node to detect apriltag markers on the camera stream at 12MP. ... This example requires the DepthAI v3 API, see",
      "title": "AprilTags from camera (12MP)",
      "url": "https://docs.luxonis.com/software-v3/depthai/examples/april_tags/april_tags_12mp"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn3search7",
      "snippet": "This configuration is then applied to a `PointCloud` node within the DepthAI pipeline.",
      "title": "PointCloudConfig",
      "url": "https://docs.luxonis.com/software/depthai-components/messages/pointcloud_config/"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn3search8",
      "snippet": "* Organized vs filtered — When `setOrganized(true)` is used on the PointCloud node, `getWidth()` / `getHeight()` match the source depth frame dimensions and include invalid",
      "title": "PointCloudData",
      "url": "https://docs.luxonis.com/software-v3/depthai/depthai-components/messages/pointcloud_data"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn3search9",
      "snippet": "When the upstream node is a `SpatialDetectionNetwork`, each tracklet also carries `spatialCoordinates` (X/Y/Z in mm), and the tracker can estimate optional 3D `velocity` and `speed`.",
      "title": "ObjectTracker",
      "url": "https://docs.luxonis.com/software-v3/depthai/depthai-components/nodes/object_tracker"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn3search10",
      "snippet": "They are also a great starting point for the DepthAI API, as different node functionalities are presented with code. ... * AprilTags - Run AprilTag",
      "title": "Depthai Examples",
      "url": "https://docs.luxonis.com/software-v3/depthai/examples/"
    },
    {
      "type": "text_result",
      "domain": "docs.luxonis.com",
      "ref_id": "turn3search11",
      "snippet": "Internally, DepthAI computes this by chaining two origin transforms: ... For example, the PointCloud node lets you receive point cloud data directly in any housing",
      "title": "Coordinate Systems",
      "url": "https://docs.luxonis.com/software-v3/depthai/depthai-components/coordinate-systems"
    },
    {
      "type": "text_result",
      "ref_id": "turn3view0",
      "snippet": "Total lines: 1",
      "title": "Internal Error"
    }
  ]
}
````

## Asistent

Camera din fotografie este **Luxonis OAK-D-Pro AF, SKU A00546**, cu procesor **RVC2**. „AF” înseamnă autofocus pentru camera RGB. [Specificațiile modelului](https://docs.luxonis.com/hardware/products/OAK-D%20Pro)

**Nu există o listă fixă de noduri de procesare care pornesc automat din fabrică.** În utilizarea obișnuită prin USB, aplicația construiește un *pipeline* — nodurile și conexiunile dintre ele — și îl încarcă în cameră împreună cu firmware-ul și resursele necesare. Așadar, „disponibil în DepthAI”, „încărcat în cameră” și „rulează” sunt trei lucruri diferite. [Funcționarea Device/Pipeline](https://docs.luxonis.com/software-v3/ai-inference/conversion/rvc-conversion/offline/)

**Ce este implicit și ce trebuie activat**

| Componentă / funcție | Starea implicită, fără un pipeline al aplicației |
|---|---|
| Captură RGB | Nu există un flux de aplicație pornit automat; trebuie configurat nodul camerei |
| Captură stereo stânga/dreapta | Trebuie configurate nodurile camerelor |
| Calcul adâncime | Nu pornește doar prin conectarea camerei; trebuie `StereoDepth` |
| Inferență AI / detecție obiecte | Nu există un model universal pornit; aplicația trebuie să furnizeze modelul și nodurile |
| Tracking, procesare imagine, codare video | Se execută dacă sunt incluse și alimentate cu date în pipeline |
| Date IMU | Aplicația trebuie să configureze nodul și rapoartele dorite |
| Proiector IR cu puncte | **Oprit implicit** |
| Iluminator IR | **Oprit implicit** |

Ultimele două sunt dispozitive hardware controlate prin API, **nu noduri separate**. Luxonis confirmă explicit că ambele sunt oprite implicit. [Controlul IR](https://docs.luxonis.com/hardware/products/OAK-D%20Pro)

**Ce se poate executa pe procesorul camerei**

Tabelul de mai jos este un inventar al principalelor funcții disponibile, **nu lista confirmată a nodurilor încărcate în aplicația voastră**. Numele și disponibilitatea exactă depind de versiunea DepthAI.

| Nod / familie de noduri | Ce face în cameră |
|---|---|
| `Camera`; în API-ul v2, `ColorCamera`, `MonoCamera` | Captură RGB și monocromă |
| `StereoDepth` | Rectificare stereo, disparitate, adâncime și filtrare configurată |
| `ImageManip` | Redimensionare, decupare și transformări de imagine |
| `NeuralNetwork` | Inferență cu un model compatibil RVC2, încărcat de aplicație |
| Noduri de detecție, inclusiv variantele YOLO/MobileNet din v2 | Inferență și interpretarea detecțiilor, conform versiunii API |
| `SpatialLocationCalculator` | Coordonate XYZ pentru regiuni din harta de adâncime |
| `ObjectTracker` | Urmărirea obiectelor detectate |
| `FeatureTracker` | Detectarea și urmărirea punctelor caracteristice |
| `EdgeDetector` | Detectarea contururilor |
| `VideoEncoder` | Codare H.264, H.265 sau MJPEG |
| `IMU` | Citirea senzorilor inerțiali |
| `Script` | Logică personalizată în mediul Python limitat al camerei |
| `Sync`, `MessageDemux` | Sincronizarea și separarea mesajelor |
| `SystemLogger` | Telemetrie despre dispozitiv |
| `XLinkIn`, `XLinkOut`, în special în v2 | Transferul datelor între calculator și cameră |

Aceste funcții folosesc diferite resurse ale RVC2: procesoare, acceleratoare de imagine, stereo și AI. Nu toate rulează pe același nucleu CPU. [Arhitectura RVC2](https://docs.luxonis.com/hardware/platform/rvc/rvc2), [API-ul nodurilor](https://docs.luxonis.com/software-v3/depthai/api/cpp)

**Pentru scanare 3D, contează mult ce rămâne pe calculator:**

- În documentația actuală DepthAI v3, `PointCloud` rulează **pe calculator pentru RVC2**. Faptul că adâncimea este calculată în cameră nu înseamnă că și norul de puncte este calculat acolo. [PointCloud](https://docs.luxonis.com/software-v3/depthai/depthai-components/host_nodes/pointcloud)
- `RGBD` procesează datele pe host, iar `AprilTag` rulează tot pe calculator la RVC2. [RGBD](https://docs.luxonis.com/software-v3/depthai/depthai-components/nodes/rgbd), [AprilTag](https://docs.luxonis.com/software-v3/depthai/depthai-components/nodes/april_tag)
- Nodurile host precum `BasaltVIO` și `RTABMapSLAM` folosesc calculatorul conectat prin USB. [Host Nodes](https://docs.luxonis.com/software-v3/depthai/depthai-components/host_nodes)

**Se pot adăuga ulterior?** Da, prin modificarea pipeline-ului și, unde este cazul, furnizarea modelelor AI. Nu sunt neapărat module deja încărcate care așteaptă un buton „Pornit”. Adăugarea unui nod poate necesita recrearea pipeline-ului; unele setări ale nodurilor existente pot fi schimbate în timpul funcționării.

**Lista completă pentru aplicația voastră rămâne de verificat:** unitatea `S:\3dscan.eva-org.com` nu este vizibilă în această sesiune, nici după încercarea cu acces extins. Am nevoie de o cale accesibilă către proiect sau de fișierul care construiește pipeline-ul și versiunea DepthAI. Din acestea pot determina exact: **nod, loc de execuție, încărcat la pornire, condiție de activare și funcții disponibile ulterior**.
