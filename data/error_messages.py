# error_messages.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-

ERROR_MESSAGES = {
    # ==========================================
    # 💀 致命系统错误 (Fatal System Errors)
    # ==========================================
    'fatal': [
        "KERNEL_PANIC: system halted",
        "SYSTEM_HALT: CPU exception",
        "CRITICAL: memory corruption detected",
        "FATAL_OOM: process killed",
        "SIGSEGV: invalid memory access",
        "DOUBLE_FAULT: shutdown requested",
        "TRIPLE_FAULT: system reset",
        "WATCHDOG_TIMEOUT: no heartbeat",
        "STACK_SMASHING detected",
        "KERNEL: NULL pointer dereference",
        "IRQ_NOT_HANDLED: interrupt storm",
        "FATAL: CPU thermal trip",
        "MACHINE_CHECK_EXCEPTION",
        "BUS_ERROR: unaligned access",
        "GENERAL_PROTECTION_FAULT",
        "DIVIDE_BY_ZERO exception",
        "INVALID_OPCODE: illegal instruction",
        "SEGMENTATION_FAULT: core dumped",
        "ABORT: assertion failed",
        "FATAL: recursive fault",
        "KERNEL: double fault loop",
        "SYSTEM: unrecoverable error",
        "CPU: microcode update failed",
        "FATAL: ACPI error",
        "KERNEL: module load failed"
    ],

    # ==========================================
    # 🔐 哈希校验失败 (Hash/Checksum Errors)
    # ==========================================
    'hash': [
        "HASH_MISMATCH: checksum failed",
        "INTEGRITY_VIOLATION: SHA256 mismatch",
        "SIGNATURE_VERIFICATION_FAILED",
        "CERTIFICATE_EXPIRED: validation failed",
        "KEY_VERIFICATION_FAILED",
        "DIGITAL_SIGNATURE_INVALID",
        "CHECKSUM_ERROR: data corruption",
        "HMAC_AUTH_FAILED: bad MAC",
        "PGP_SIG: bad signature",
        "TLS_HANDSHAKE: cert invalid",
        "SECURE_BOOT: signature error",
        "UEFI: secure violation",
        "MD5_CHECKSUM: mismatch",
        "CRC32_ERROR: data corrupted",
        "SHA1_HASH: collision detected",
        "INTEGRITY_CHECK: failed",
        "MANIFEST_VERIFICATION: failed",
        "PACKAGE_INTEGRITY: compromised",
        "FINGERPRINT_MISMATCH",
        "DIGEST_VERIFICATION: failed"
    ],

    # ==========================================
    # 🔑 密钥与证书错误 (Key/Certificate Errors)
    # ==========================================
    'key': [
        "KEY_EXPIRED: certificate expired",
        "KEY_REVOKED: key in CRL",
        "KEY_ATTESTATION_FAILED",
        "PRIVATE_KEY_LOCKED: access denied",
        "PUBLIC_KEY_INVALID: malformed",
        "ENCRYPTION_KEY_MISSING",
        "DECRYPTION_FAILED: bad key",
        "KEY_STORE_CORRUPTED",
        "TPM: key not found",
        "HSM: key unavailable",
        "KEY_ROTATION_FAILED",
        "SECURE_ENCLAVE: key invalid",
        "KEY_DERIVATION: failed",
        "KEY_EXCHANGE: parameter invalid",
        "CERTIFICATE_CHAIN: broken",
        "ROOT_CA: untrusted",
        "INTERMEDIATE_CA: revoked",
        "KEY_USAGE: violation",
        "KEY_LIFETIME: exceeded",
        "KEY_BACKUP: failed"
    ],

    # ==========================================
    # 🚫 认证与授权错误 (Auth/Authorization Errors)
    # ==========================================
    'auth': [
        "AUTH_FAILED: invalid credentials",
        "ACCESS_DENIED: permission denied",
        "UNAUTHORIZED_ACCESS: audit logged",
        "SESSION_EXPIRED: reauth required",
        "TOKEN_INVALID: malformed JWT",
        "MFA_REQUIRED: second factor",
        "CAPABILITY_DENIED: insufficient",
        "PRIVILEGE_ESCALATION_FAILED",
        "USER_NOT_AUTHENTICATED",
        "RBAC: insufficient privileges",
        "SELINUX: AVC denial",
        "APPARMOR: profile violation",
        "PAM: authentication failure",
        "LDAP_BIND: invalid dn",
        "KERBEROS: ticket expired",
        "OAUTH2: invalid grant",
        "SAML: assertion invalid",
        "API_KEY: invalid or revoked",
        "RATE_LIMIT: exceeded",
        "ACCOUNT_LOCKED: too many attempts"
    ],

    # ==========================================
    # 🌐 网络与连接错误 (Network/Connection Errors)
    # ==========================================
    'network': [
        "CONNECTION_TIMEOUT: no response",
        "NETWORK_UNREACHABLE: host down",
        "DNS_RESOLUTION_FAILED: nxdomain",
        "SSL_HANDSHAKE_FAILED: protocol error",
        "PEER_RESET_CONNECTION: RST",
        "TCP_SYN_RETRANSMIT: timeout",
        "ROUTE_NOT_FOUND: no route to host",
        "GATEWAY_UNREACHABLE: ICMP unreach",
        "PORT_SCAN_DETECTED: blocked",
        "DDOS_MITIGATION triggered",
        "FIREWALL: packet dropped",
        "IDS: intrusion detected",
        "DHCP_LEASE: expired",
        "ARP_RESOLUTION: failed",
        "MTU_PROBLEM: packet too big",
        "TCP_SEQ: out of window",
        "IP_FRAGMENT: assembly failed",
        "TLS_VERSION: unsupported",
        "CIPHER_SUITE: no shared",
        "CERTIFICATE_HOSTNAME: mismatch"
    ],

    # ==========================================
    # 💾 硬件错误 (Hardware Errors)
    # ==========================================
    'hardware': [
        "DISK_READ_ERROR: sector unreadable",
        "DISK_WRITE_FAILED: media error",
        "SATA_LINK_DOWN: device offline",
        "NVME: controller fatal error",
        "PCIe: uncorrectable error",
        "GPU_RESET: TDR detected",
        "MEMORY_ECC_ERROR: uncorrectable",
        "CPU_MACHINE_CHECK_EXCEPTION",
        "POWER_LOSS: capacitor failure",
        "FAN_FAILURE: thermal throttling",
        "VOLTAGE_REGULATOR: undervoltage",
        "I2C_BUS: device not responding",
        "SPI_FLASH: write protected",
        "DMA: transfer failed",
        "IRQ_CONFLICT: sharing violation",
        "IOMMU: page fault",
        "SMART: disk failing",
        "REALLOCATED_SECTOR: count exceeded",
        "PENDING_SECTOR: unstable",
        "UDMA_CRC_ERROR: cable problem"
    ],

    # ==========================================
    # 📁 文件系统错误 (Filesystem Errors)
    # ==========================================
    'filesystem': [
        "FS_CORRUPTION: inode error",
        "JOURNAL_RECOVERY_FAILED",
        "SUPERBLOCK_READ_ERROR: mount failed",
        "EXT4: filesystem corrupted",
        "XFS: metadata corruption",
        "BTRFS: checksum mismatch",
        "ZFS: IO failure",
        "NTFS: volume dirty",
        "FAT: cluster chain broken",
        "QUOTA_EXCEEDED: no space left",
        "INODE_TABLE_CORRUPT",
        "DIRECTORY_CORRUPT: lost+found",
        "FILE_SYSTEM: readonly",
        "DISK_FULL: write failed",
        "FILE_TOO_LARGE: fs limit",
        "TOO_MANY_OPEN_FILES",
        "LOCK_CONTENTION: deadlock",
        "DIR_NOT_EMPTY: rmdir failed",
        "CROSS_DEVICE_LINK: invalid",
        "FILE_EXISTS: already there"
    ],

    # ==========================================
    # 🗄️ 数据库错误 (Database Errors)
    # ==========================================
    'database': [
        "DB_CONNECTION_FAILED: timeout",
        "TRANSACTION_DEADLOCK: rollback",
        "TABLE_CORRUPT: rebuilding",
        "INDEX_CORRUPTION: dropping index",
        "REPLICATION_LAG: sync failed",
        "QUERY_TIMEOUT: killed by watchdog",
        "BUFFER_POOL_EXHAUSTED: OOM",
        "WAL_ARCHIVE_FAILED: no space",
        "CHECKPOINT_FAILED: dirty pages",
        "VACUUM_FULL: no space",
        "REDO_LOG_CORRUPT: recovery failed",
        "TABLESPACE_CORRUPT: data loss",
        "DATABASE_LOCKED: in use",
        "CONSTRAINT_VIOLATION: FK failed",
        "UNIQUE_VIOLATION: duplicate key",
        "DEADLOCK_DETECTED: victim chosen",
        "CONNECTION_LIMIT: exceeded",
        "PREPARED_STATEMENT: not found",
        "CURSOR_INVALID: already closed",
        "TRANSACTION_LOG: full"
    ],

    # ==========================================
    # 🛡️ 安全警告 (Security Warnings)
    # ==========================================
    'security': [
        "INTRUSION_DETECTED: port scan",
        "BRUTE_FORCE_ATTACK: rate limiting",
        "BUFFER_OVERFLOW: DEP prevented",
        "ROP_CHAIN DETECTED: process killed",
        "ASLR_BYPASS ATTEMPT: blocked",
        "CODE_INJECTION DETECTED",
        "PRIVILEGE_ESCALATION: audit",
        "CONTAINER_ESCAPE: seccomp violation",
        "KASLR: information leak",
        "SPECTRE_V2: mitigation triggered",
        "MELTDOWN: kernel page leak",
        "SHELLCODE_DETECTED: SIGKILL",
        "RET2LIBC: return oriented",
        "STACK_COOKIE: corrupted",
        "HEAP_CORRUPTION: free invalid",
        "USE_AFTER_FREE: dangling pointer",
        "DOUBLE_FREE: memory corruption",
        "FORMAT_STRING: exploit attempt",
        "SQL_INJECTION: query blocked",
        "XSS: script injection blocked"
    ],

    # ==========================================
    # 🔒 加密错误 (Cryptography Errors)
    # ==========================================
    'crypto': [
        "RNG_ENTROPY_LOW: blocking",
        "ENCRYPTION_ENGINE_FAILED",
        "DECRYPTION_BUFFER_OVERFLOW",
        "AES_NI: instruction unavailable",
        "RSA_OPERATION_FAILED: key size",
        "EC_CURVE: invalid parameters",
        "DH_KEY_EXCHANGE: weak parameters",
        "RANDOM_POOL: insufficient entropy",
        "CSPRNG: reseed required",
        "TLS: PRF calculation failed",
        "PKCS7: padding error",
        "CRYPTO_ACCEL: hardware error",
        "KEY_GENERATION: failed",
        "RANDOM_DEVICE: blocking",
        "ENTROPY_SOURCE: depleted",
        "DRBG: instantiate failed",
        "CRYPTO_CONTEXT: corrupted",
        "IV_REUSE: security violation",
        "NONCE: already used",
        "AEAD_TAG: verification failed"
    ],

    # ==========================================
    # ⚙️ 运行时错误 (Runtime Errors)
    # ==========================================
    'runtime': [
        "OUT_OF_MEMORY: allocation failed",
        "STACK_OVERFLOW: recursion depth",
        "HEAP_EXHAUSTED: no free blocks",
        "INVALID_POINTER: dereference",
        "DIVISION_BY_ZERO: arithmetic",
        "OVERFLOW: integer overflow",
        "UNDERFLOW: integer underflow",
        "FLOAT_EXCEPTION: inexact",
        "BAD_SYSCALL: invalid number",
        "ILLEGAL_INSTRUCTION: opcode",
        "ALIGNMENT_CHECK: unaligned access",
        "CONTEXT_SWITCH: heavy load",
        "SCHEDULER: starvation detected",
        "TIMER_SLIPPAGE: missed deadline",
        "WORKER_POOL: exhausted",
        "TASK_HUNG: watchdog reset",
        "DEADLOCK: circular wait",
        "RACE_CONDITION: detected",
        "LIVE_LOCK: no progress",
        "PRIORITY_INVERSION: detected"
    ],

    # ==========================================
    # 🔌 驱动与设备错误 (Driver/Device Errors)
    # ==========================================
    'driver': [
        "DEVICE_NOT_FOUND: missing",
        "DRIVER_LOAD_FAILED: init error",
        "USB_DEVICE: disconnected",
        "PCI_CONFIG: read failed",
        "I2C_TRANSFER: NAK received",
        "SPI_COMMUNICATION: timeout",
        "UART_FRAMING: parity error",
        "DMA_BUFFER: alignment error",
        "INTERRUPT_STORM: throttling",
        "MMIO: invalid access",
        "REGISTER_WRITE: failed",
        "FIRMWARE_LOAD: corrupted",
        "DEVICE_HUNG: resetting",
        "LINK_TRAINING: failed",
        "PHY_ERROR: link down",
        "HOTPLUG: removal detected",
        "POWER_MANAGEMENT: suspend fail",
        "WAKEUP: interrupt storm",
        "DEVICE_REMOVED: surprise",
        "RESOURCE_CONFLICT: IRQ/IO"
    ],

    # ==========================================
    # 📊 监控与指标错误 (Monitoring/Metrics Errors)
    # ==========================================
    'monitoring': [
        "CPU_THROTTLED: thermal limit",
        "MEMORY_PRESSURE: high",
        "DISK_IO: latency spike",
        "NETWORK_JITTER: high variance",
        "PACKET_LOSS: exceeding threshold",
        "LATENCY_SPIKE: >100ms",
        "ERROR_RATE: increasing",
        "HEALTH_CHECK: failed",
        "PROBE_FAILED: endpoint down",
        "METRIC_INGEST: backlog",
        "ALERT_MANAGER: notification fail",
        "GRAFANA: datasource error",
        "PROMETHEUS: target down",
        "LOGS: index rate limited",
        "TRACE_SAMPLING: queue full",
        "APM: agent disconnected",
        "PROFILER: data corrupted",
        "MONITORING: agent dead",
        "TELEMETRY: export failed",
        "HEARTBEAT: missed"
    ],

    # ==========================================
    # 🤖 机器学习错误 (Machine Learning Errors) - 新增
    # ==========================================
    'ml': [
        # 训练错误
        "TRAINING_DIVERGED: loss = NaN",
        "GRADIENT_EXPLOSION: value > 1e6",
        "GRADIENT_VANISHING: near zero",
        "LEARNING_RATE_TOO_HIGH: oscillating",
        "BATCH_SIZE_MISMATCH: last batch",
        "EPOCH_INTERRUPTED: early stop",
        "EARLY_STOPPING: no improvement",
        "UNDERFITTING: high bias detected",
        "OVERFITTING: train/val gap > 30%",

        # 模型加载/保存错误
        "MODEL_LOAD_FAILED: version mismatch",
        "MODEL_CORRUPTED: weights mismatch",
        "CHECKPOINT_LOAD: tensor shape mismatch",
        "SAVED_MODEL: incompatible format",
        "WEIGHT_INITIALIZATION_FAILED",

        # 数据错误
        "DATA_LOADER: worker crashed",
        "DATASET_CORRUPT: missing labels",
        "DATA_AUGMENTATION: pipeline error",
        "TRAIN_TEST_SPLIT: label imbalance",
        "CLASS_IMBALANCE: severe skew",
        "FEATURE_SCALING: failed",
        "NORMALIZATION: zero variance",
        "DATA_LEAKAGE: time series contaminated",
        "MISSING_VALUES: imputation failed",

        # 张量/形状错误
        "TENSOR_SHAPE_MISMATCH: expected [B,3,224,224]",
        "DIMENSION_MISMATCH: cannot broadcast",
        "OUT_OF_MEMORY: CUDA OOM",
        "CUDA_ERROR: device side assert",
        "CUDA_LAUNCH_FAILED: kernel error",
        "CUDA_SYNC: timeout",
        "TENSOR_ON_WRONG_DEVICE: CPU vs GPU",
        "PIN_MEMORY: allocation failed",

        # 层/网络错误
        "LAYER_NOT_INITIALIZED: forward pass",
        "ACTIVATION_NAN: relu dead neuron",
        "SOFTMAX: overflow in exponent",
        "CROSS_ENTROPY: logits instability",
        "BATCH_NORM: running stats corrupted",
        "DROPOUT: inference/train mismatch",
        "CONV_WEIGHTS: filter size mismatch",
        "POOLING_LAYER: stride > kernel",

        # 优化器错误
        "OPTIMIZER_STEP: parameter update failed",
        "ADAM: epsilon too small",
        "SGD_MOMENTUM: velocity overflow",
        "LR_SCHEDULER: decay factor < 0",
        "GRADIENT_CLIPPING: global norm inf",
        "WEIGHT_DECAY: value too high",

        # 损失函数错误
        "LOSS_NAN: numerical instability",
        "LOSS_INFINITY: divergence detected",
        "NEGATIVE_LOG_LIKELIHOOD: invalid input",
        "HUBER_LOSS: delta parameter invalid",
        "FOCAL_LOSS: gamma too high",

        # 评估错误
        "METRIC_COMPUTATION: division by zero",
        "ACCURACY: all predictions same",
        "PRECISION/RECALL: undefined",
        "F1_SCORE: division by zero",
        "CONFUSION_MATRIX: size mismatch",
        "AUC_SCORE: only one class present",

        # 推理错误
        "INFERENCE_TIMEOUT: >100ms budget",
        "BATCH_INFERENCE: mixed shapes",
        "MODEL_WARMUP: failed",
        "ONNX_RUNTIME: graph optimization failed",
        "TENSORRT: engine build failed",
        "QUANTIZATION: calibration failed",
        "PRUNING: mask generation failed",
        "DISTILLATION: teacher/student mismatch",

        # 分布式训练错误
        "DDP: rank mismatch",
        "HOROVOD: allreduce failed",
        "NCCL: communication error",
        "GLOO: socket timeout",
        "TORCHRUN: world size mismatch",
        "MULTI_GPU: device mapping error",
        "SYNC_BATCH_NORM: all_gather failed",

        # 特定框架错误
        "PYTORCH: CUDA out of memory",
        "TENSORFLOW: GPU device error",
        "JAX: XLA compilation failed",
        "KERAS: model not built",
        "MXNET: ndarray error",
        "CAFFE2: workspace error",
        "ONNX: unsupported operator",
        "TVM: relay build failed"
    ],

    # ==========================================
    # 📚 堆栈跟踪错误 (Stack Trace/Backtrace Errors) - 新增
    # ==========================================
    'stack': [
        # 堆栈溢出/错误
        "STACK_OVERFLOW: recursive call depth 1024",
        "STACK_UNDERFLOW: pop from empty stack",
        "STACK_CORRUPTION: canary check failed",
        "STACK_SMASHING: return address overwritten",
        "STACK_BUFFER_OVERFLOW: local variable",
        "STACK_FRAME: corrupted by alloca",
        "STACK_GUARD: terminated process",
        "STACK_TRACE: incomplete traceback",

        # 函数调用栈
        "CALL_STACK: max depth exceeded",
        "FUNCTION_CALL: too many arguments",
        "RECURSION_LIMIT: depth 1000 reached",
        "TAIL_CALL_OPTIMIZATION: failed",
        "CALLBACK_LOOP: infinite recursion",
        "VIRTUAL_CALL: pure function called",
        "FUNCTION_SIG: mismatch in call",

        # 栈帧错误
        "FRAME_POINTER: corrupted",
        "BASE_POINTER: invalid address",
        "RETURN_ADDRESS: pointing to garbage",
        "STACK_UNWIND: failed in exception",
        "BACKTRACE: symbol resolution failed",
        "STACK_WALK: incomplete frames",
        "FRAME_CHAIN: broken linkage",

        # 异常处理
        "EXCEPTION_UNWIND: catch block not found",
        "TERMINATE: no active exception",
        "UNCAUGHT_EXCEPTION: terminating",
        "EH_FRAME: corrupted unwind info",
        "CATCH_ALL: caught unknown exception",
        "EXCEPTION_RE_THROW: bad exception",

        # 内存/栈分配
        "STACK_ALLOC: alloca failed",
        "VL_ARRAY: stack size > limit",
        "STACK_EXTENSION: guard page hit",
        "STACK_COMMIT: page fault",
        "STACK_GROWTH: exceeds rlimit",
        "STACK_MMAP: allocation failed",

        # 调试信息
        "DWARF_DEBUG: line info missing",
        "SYMBOL_TABLE: corrupted",
        "STACK_FRAME_INFO: not available",
        "DEBUG_SYMBOLS: stripped binary",
        "SOURCE_MAP: invalid mapping",
        "LINE_NUMBER: out of range",

        # 栈回溯格式
        "BACKTRACE: [0x7FFF1234] main+0x24",
        "BACKTRACE: [0x7FFF5678] func_a+0x12",
        "BACKTRACE: [0x7FFF9ABC] func_b+0x8",
        "BACKTRACE: [0x7FFFDEAD] _start+0x2e",
        "STACK_TRACE: #0 0xDEADBEEF in malloc",
        "STACK_TRACE: #1 0xBAADF00D in operator new",
        "STACK_TRACE: #2 0xCAFEBABE in std::vector",
        "STACK_TRACE: #3 0xFEEDFACE in main",

        # 特定语言错误
        "RUST: panic at 'index out of bounds'",
        "RUST: unwinding panicked",
        "RUST: double panic detected",
        "GO: stack overflow in goroutine",
        "GO: panic: runtime error",
        "JAVA: StackOverflowError",
        "JAVA: NullPointerException at line 42",
        "PYTHON: RecursionError: max depth",
        "PYTHON: Traceback (most recent call last)",
        "PYTHON: File \"main.py\", line 1337, in <module>",
        "C#: StackOverflowException",
        "C#: NullReferenceException",
        "JAVASCRIPT: Maximum call stack exceeded",
        "JAVASCRIPT: Uncaught RangeError",
        "LUA: stack overflow in C function",
        "PHP: Fatal error: Nesting level too deep",

        # 内核堆栈
        "KERNEL_STACK: overflow in syscall",
        "KERNEL_STACK: IRQ stack corrupted",
        "KERNEL_STACK: double fault in handler",
        "KERNEL_STACK: exception stack overflow",
        "KERNEL_STACK: process context switch failed",

        # 堆栈跟踪示例
        "CALL_TRACE: thread 0x7F1234 crashed",
        "STACK_DUMP: RIP=0xDEADBEEF RSP=0xCAFE",
        "FRAME_POINTER: RBP=0xBAADF00D",
        "STACK_CONTENT: [0xFFFF] [0xDEAD] [0xBEEF]",
        "STACK_TOP: 0x7FFE1234, STACK_BASE: 0x7FFEABCD",

        # 线程错误
        "THREAD_STACK: TLS corruption",
        "THREAD_LOCAL: storage exhausted",
        "FIBER_STACK: context switch failed",
        "COROUTINE_STACK: resumption failed",
        "ASYNC_STACK: future not ready",

        # 堆栈分析
        "STACK_ANALYSIS: cycle detected in call graph",
        "STACK_PROFILER: sampling overflow",
        "STACK_TRACING: disabled in release build",
        "STACK_DUMP: incomplete due to optimization",
        "STACK_WALK: frame pointer omitted (-fomit)"
    ],

    # ==========================================
    # 🔬 深度学习框架特定错误 (Deep Learning Framework Errors) - 新增
    # ==========================================
    'dl_framework': [
        # PyTorch
        "TORCH: CUDA out of memory (OOM)",
        "TORCH: tensor on wrong device",
        "TORCH: gradient computation failed",
        "TORCH: autograd engine deadlock",
        "TORCH: DataLoader worker crashed",
        "TORCH: DDP communication error",
        "TORCH: checkpoint load failed",
        "TORCH: JIT compilation failed",
        "TORCH: FX graph transformation error",

        # TensorFlow
        "TF: GPU device not found",
        "TF: graph execution error",
        "TF: eager execution disabled",
        "TF: gradient tape context error",
        "TF: Keras model not built",
        "TF: dataset iterator exhausted",
        "TF: checkpoint restore failed",
        "TF: XLA compilation timeout",
        "TF: TensorBoard logging failed",

        # JAX
        "JAX: XLA compilation failed",
        "JAX: PMAP sharding error",
        "JAX: device array conversion",
        "JAX: Tracer leaked to host",
        "JAX: pure function violated",
        "JAX: vmap batching error",
        "JAX: grad of grad not allowed",

        # ONNX
        "ONNX: model validation failed",
        "ONNX: unsupported operator",
        "ONNX: shape inference error",
        "ONNX: external data missing",
        "ONNX: optimizer graph pass failed"
    ]
}

# ==========================================
# 📝 BIOS/UEFI 风格错误消息 (简短的)
# ==========================================
BIOS_ERRORS = {
    'beep_codes': [
        "1 long 2 short: Video error",
        "1 long 3 short: Memory error",
        "Continuous beeps: Power error",
        "High frequency: CPU overheat",
        "1 short: POST passed",
        "2 short: POST failed",
        "3 long: Keyboard error",
        "1 long: Memory refresh",
        "2 long: Parity circuit",
        "3 long: Base 64K memory"
    ],

    'post_codes': [
        "POST 0x00: CPU init",
        "POST 0x01: Cache init",
        "POST 0x02: Memory test",
        "POST 0x03: Video BIOS",
        "POST 0x04: Keyboard init",
        "POST 0x05: Floppy seek",
        "POST 0x06: Hard disk",
        "POST 0x07: Boot device",
        "POST 0x08: CMOS verify",
        "POST 0x09: DMA init",
        "POST 0x0A: IRQ init",
        "POST 0x0B: Timer test",
        "POST 0x0C: Real time clock",
        "POST 0x0D: Serial ports",
        "POST 0x0E: Parallel ports",
        "POST 0x0F: Math coprocessor"
    ],

    'cmos_errors': [
        "CMOS checksum error",
        "CMOS battery low",
        "CMOS time invalid",
        "CMOS config corrupted",
        "CMOS data mismatch",
        "CMOS memory size error",
        "CMOS disk type error",
        "CMOS display type error"
    ],

    'uefi_errors': [
        "UEFI: Secure boot violation",
        "UEFI: Boot variable corrupted",
        "UEFI: Image verification failed",
        "UEFI: Driver signing error",
        "UEFI: Protocol not found",
        "UEFI: Memory map corrupted",
        "UEFI: GPT header invalid",
        "UEFI: Boot order corrupted"
    ]
}

# ==========================================
# 🎯 短格式错误码 (适合在小框内显示)
# ==========================================
SHORT_ERROR_CODES = [
    "ERR_001", "ERR_002", "ERR_003", "ERR_004", "ERR_005",
    "E_BADF", "E_NOENT", "E_IO", "E_BUSY", "E_TIMEOUT",
    "E_AGAIN", "E_NOMEM", "E_ACCES", "E_FAULT", "E_EXIST",
    "E_INVAL", "E_MFILE", "E_PIPE", "E_ROFS", "E_SPIPE",
    "E_NOSPC", "E_MCHK", "E_PWR", "E_BADMSG", "E_IDRM",
    "FATAL:001", "FATAL:00A", "FATAL:0FF", "FATAL:DEAD",
    "PANIC:001", "PANIC:00F", "PANIC:0C0", "PANIC:0DE",
    "ABRT:001", "ABRT:002", "ABRT:0FF", "ABRT:0xDEAD",
    "HALT:001", "HALT:0FF", "HALT:0xDE", "HALT:0xAD",
    "0xC0000005", "0xC0000008", "0xC0000017", "0xC0000022",
    "0xDEADBEEF", "0xBAADF00D", "0xCAFEBABE", "0xFEEDFACE",
    "CUDA:001", "CUDA:002", "CUDA:OOM", "CUDA:ERR",
    "ML:001", "ML:002", "ML:OVERFIT", "ML:UNDERFIT",
    "STACK:OVF", "STACK:UND", "STACK:SMASH"
]


# ==========================================
# 📋 获取错误消息的函数
# ==========================================
def get_random_error(category=None):
    """获取随机错误消息

    Args:
        category: 指定类别，如 'fatal', 'hash', 'ml', 'stack' 等，None则随机选择

    Returns:
        随机错误消息字符串
    """
    import random

    if category is None:
        category = random.choice(list(ERROR_MESSAGES.keys()))

    if category in ERROR_MESSAGES:
        return random.choice(ERROR_MESSAGES[category])
    else:
        return f"UNKNOWN_ERROR: {category}"


def get_random_short_code():
    """获取随机短错误码"""
    import random
    return random.choice(SHORT_ERROR_CODES)


def get_random_bios_error(error_type=None):
    """获取随机BIOS错误

    Args:
        error_type: 'beep_codes', 'post_codes', 'cmos_errors', 'uefi_errors'
    """
    import random

    if error_type is None:
        error_type = random.choice(list(BIOS_ERRORS.keys()))

    if error_type in BIOS_ERRORS:
        return random.choice(BIOS_ERRORS[error_type])
    else:
        return f"BIOS_ERROR: {error_type}"


def format_error_with_hex(error_msg, hex_addr=None):
    """格式化错误消息，添加十六进制地址"""
    import random

    if hex_addr is None:
        hex_addr = f"0x{random.randint(0, 0xFFFFFF):06X}"

    return f"{error_msg} at {hex_addr}"


def format_error_with_code(error_msg, error_code=None):
    """格式化错误消息，添加错误码"""
    import random

    if error_code is None:
        error_code = random.choice(SHORT_ERROR_CODES)

    return f"[{error_code}] {error_msg}"


def format_stack_trace(func_name=None, line_num=None):
    """格式化堆栈跟踪行"""
    import random

    if func_name is None:
        func_names = [
            "main", "_start", "malloc", "free", "operator_new",
            "std::vector::push_back", "std::map::insert",
            "PyEval_EvalFrameEx", "torch::autograd::Engine::execute",
            "tensorflow::OpKernel::Compute", "cudaLaunchKernel"
        ]
        func_name = random.choice(func_names)

    if line_num is None:
        line_num = random.randint(1, 9999)

    addr = f"0x{random.randint(0, 0x7FFFFFFF):08X}"

    formats = [
        f"  at {func_name}() +0x{random.randint(0, 0xFF):02X}",
        f"  #{random.randint(0, 20)} {addr} in {func_name} (line {line_num})",
        f"  [0x{random.randint(0, 0xFFFF):04X}] {func_name}+0x{random.randint(0, 0xFF):02X}",
        f"  -> {func_name} at {line_num}:{random.randint(1, 100)}",
        f"  from {func_name}:{line_num} (0x{addr})"
    ]

    return random.choice(formats)


def get_random_ml_error(subcategory=None):
    """获取随机机器学习错误"""
    import random

    if subcategory is None:
        return random.choice(ERROR_MESSAGES['ml'])

    ml_errors_by_type = {
        'training': [e for e in ERROR_MESSAGES['ml'] if 'TRAIN' in e or 'EPOCH' in e or 'GRADIENT' in e],
        'inference': [e for e in ERROR_MESSAGES['ml'] if 'INFERENCE' in e or 'BATCH' in e],
        'cuda': [e for e in ERROR_MESSAGES['ml'] if 'CUDA' in e or 'GPU' in e],
        'data': [e for e in ERROR_MESSAGES['ml'] if 'DATA' in e or 'DATASET' in e],
        'model': [e for e in ERROR_MESSAGES['ml'] if 'MODEL' in e or 'LAYER' in e],
        'optimizer': [e for e in ERROR_MESSAGES['ml'] if 'OPTIMIZER' in e or 'GRADIENT' in e],
    }

    if subcategory in ml_errors_by_type and ml_errors_by_type[subcategory]:
        return random.choice(ml_errors_by_type[subcategory])

    return random.choice(ERROR_MESSAGES['ml'])