// EVA-3dScan: proposed domain contracts, NOT an implemented or compiled iOS app.
// Pin Swift/Xcode/SDK at W00. No Apple camera API signature is invented here.
import Foundation

public enum CaptureMode: String, Codable, Sendable {
    case objectPersistent = "object_persistent"
    case liveEphemeral = "live_ephemeral"
    case roomsPersistent = "rooms_persistent"
    case robotStream = "robot_stream"
}
public enum CaptureState: String, Codable, Sendable {
    case idle, checking, ready, capturing, suspended, finalizing, reviewing, saved, failed
}
public enum CaptureFailure: Error, Sendable {
    case deniedCamera, unsupportedCapability(String), unavailableStorage
    case trackingLimited, interrupted, thermalCritical, invalidCalibration
    case staleEpoch, resourceLimit, corruptInput, commitFailed, requiresRecapture
}
public struct RuntimeCapabilities: Sendable {
    public let hardwareIdentifier: String
    public let osBuild: String
    public let appBuild: String
    public let worldTracking: Bool
    public let sceneDepth: Bool
    public let sceneReconstruction: Bool
    public let roomCapture: Bool
    public let objectCapture: Bool
    public let photogrammetry: Bool
}
// Wire IDs follow transport.schema.json: ASCII [A-Za-z0-9_./:-], 1...96.
// A project UUID is a narrower persistent identifier; do not reinterpret frame_id
// as image identity. Epochs become canonical decimal STRINGS on the wire.
public struct CaptureIdentity: Sendable {
    public let deviceID: String
    public let sessionID: String
    public let mapEpoch: UInt64
    public let clockEpoch: UInt64
    public let calibrationID: String
    public let frameID: String
    public let observationID: String
    public let sequence: UInt64
    public let sourceCaptureTimeNS: Int64 // original iPhone monotonic domain
    public let captureTimeNS: Int64 // wire: converted Thor monotonic domain
    public let clockModelID: String
    public let uncertaintyNS: UInt64
}
// Clock conversion is required before RobotLink encoding. Before a qualified
// clock model exists, no motion-usable observation is emitted to the robot.
public struct Vector3: Codable, Sendable {
    public let x: Double
    public let y: Double
    public let z: Double
}
public struct Quaternion: Codable, Sendable {
    public let x: Double
    public let y: Double
    public let z: Double
    public let w: Double
}
// Internal typed values. Wire encoder emits arrays translation_m/quaternion_xyzw;
// the default Codable representation above is NOT the wire representation.
public struct MetricPose: Sendable {
    public let translationM: Vector3
    public let quaternionXYZW: Quaternion
}
public enum TrackState: String, Codable, Sendable {
    case observed, predicted, occluded, lost, retired
}
public enum AmbiguityStatus: String, Codable, Sendable {
    case none, pose, identity, both
}
public struct ObjectObservation: Sendable {
    // For lost/occluded, pose is historical and never motion-usable. Identity
    // retains the last contributing capture time; heartbeat carries live health.
    // Wire v1 predicted retains last observed pose AND capture time; it does
    // not carry extrapolation. Local display prediction needs separate timing.
    public let identity: CaptureIdentity
    public let objectID: String
    public let modelVersion: String
    public let state: TrackState
    public let ambiguity: AmbiguityStatus
    public let pose: MetricPose
    // nil means unestimated, never zero precision. If present: row-major 6x6,
    // order tx ty tz rx ry rz, right perturbation T=That Exp(delta), local object.
    // Validate finite, symmetric and PSD; blocks m², m.rad, rad².
    public let covariance: [Double]?
    public let covarianceFrameID: String
    public let confidence: Double
}
public struct FrameDescriptor: Sendable {
    public let identity: CaptureIdentity
    public let rgbWidth: Int
    public let rgbHeight: Int
    public let depthWidth: Int
    public let depthHeight: Int
    // Calibration at actual pixel orientation/resolution, not UI coordinates.
    public let rgbIntrinsicsRowMajor: [Double]
    public let depthIntrinsicsRowMajor: [Double]
    public let worldFromCamera: MetricPose
    public let cameraFrameID: String // optical frame for wire depth_frame
}
// Tokens carry NO CVPixelBuffer across arbitrary actor isolation. The pool's
// implementation owns camera buffers and makes scoped, validated adapter access.
// A token is copyable at the type level; the pool rejects duplicate releases and
// access after release. Swift Sendable alone does not prove lifetime correctness.
public struct FrameLease: Hashable, Sendable {
    public let token: UUID
    public let observationID: String
}
public enum FrameConsumer: Sendable { case detector, tracker, renderer, depthEncoder }
public protocol FramePool: Actor {
    func acquireLatest(for consumer: FrameConsumer) async throws -> FrameLease?
    func descriptor(for lease: FrameLease) async throws -> FrameDescriptor
    // GPU adapters retain their lease until actual command-buffer completion;
    // cancellation requests do not imply the GPU has stopped reading memory.
    func release(_ lease: FrameLease) async throws
    func invalidate(epoch: UInt64) async
}
public struct SchedulerLimits: Sendable {
    public let retainedFrames: Int // initial 3
    public let outstandingLeases: Int // initial 6
    public let queuedDetection: Int // initial 1, newest replaces old
    public let heavyPoseJobs: Int // initial 1
    public let gpuCommands: Int // initial 2
    public let ownedBufferBytes: Int // initial 201326592, excludes opaque frameworks
}
public protocol CaptureCoordinator: Actor {
    // Exclusive camera owner: stop and drain previous backend before start.
    func preflight(mode: CaptureMode) async throws -> RuntimeCapabilities
    func start(mode: CaptureMode, calibrationID: String) async throws
    func suspend(reason: String) async
    func resume() async throws
    func finish() async throws
    func cancel() async
    func state() async -> CaptureState
}
public protocol PerceptionEngine: Actor {
    func estimate(lease: FrameLease, modelIDs: [String]) async throws -> [ObjectObservation]
    func reset(sessionID: String, mapEpoch: UInt64, clockEpoch: UInt64) async
}
public struct ArtifactRef: Sendable {
    public let sha256: String
    public let byteLength: Int64 // must be >= 0; SQLite INTEGER bound
    public let mediaType: String
}
public enum JobState: String, Codable, Sendable {
    case queued, running, checkpointed, completed, failed, cancelled
    case needsRecapture = "needs_recapture"
}
public struct JobRequest: Sendable {
    public let jobID: UUID
    public let projectID: UUID
    public let inputRevision: Int64 // must be >= 0; SQLite INTEGER bound
    public let kind: String
    public let parametersSHA256: String
    public let algorithmVersion: String
    public let idempotencyKey: String
}
public struct JobCheckpoint: Sendable {
    public let jobID: UUID
    public let checkpointArtifact: ArtifactRef
    public let completedUnits: UInt64
    public let totalUnits: UInt64
}
public protocol ProjectStore: Actor {
    // Implementation: stage+hash+sync+rename CAS first, then one SQLite commit.
    // No promise of a transaction spanning SQLite and filesystem.
    func commitArtifact(projectID: UUID, stagedFile: URL, mediaType: String) async throws -> ArtifactRef
    func enqueue(_ request: JobRequest) async throws -> UUID
    func checkpoint(_ checkpoint: JobCheckpoint) async throws
    func recoverInterruptedJobs() async throws -> [UUID]
}
public enum ExportFormat: String, Codable, Sendable {
    case stl, threeMF = "3mf", ply, usdz, dxf2D = "dxf_2d", dwg
}
public struct ExportRequest: Sendable {
    public let job: JobRequest
    public let format: ExportFormat
    public let lengthUnit: String
    public let includeTextures: Bool
}
public struct ExportResult: Sendable {
    public let file: ArtifactRef
    public let report: ArtifactRef
    public let warnings: [String]
}
public protocol ExportEngine: Actor {
    func validate(request: ExportRequest) async throws -> [String]
    func execute(request: ExportRequest) async throws -> ExportResult
}
public protocol RobotLink: Actor {
    // Explicit robot_stream mode only. Actual wire validation is mandatory.
    // Realtime pose may replace old unsent pose; map delta uses acknowledged
    // revisions and never inherits that replacement policy.
    func connect(pairedEndpoint: URL, expectedPeerKeySHA256: String) async throws
    func submit(_ observation: ObjectObservation) async throws
    func pause() async
    func disconnect() async
}
public struct LiveEphemeralDependencies: Sendable {
    public let capture: any CaptureCoordinator
    public let perception: any PerceptionEngine
    public let frames: any FramePool
    // Deliberately no ProjectStore, ExportEngine or RobotLink dependency.
    // Explicit "save this annotated image" creates a separate persistent command.
}
