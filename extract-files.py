#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import extract_utils.tools
extract_utils.tools.DEFAULT_PATCHELF_VERSION = '0_17_2'

from extract_utils.file import File
from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixup_remove_arch_suffix,
    lib_fixup_remove_proto_version_suffix,
    lib_fixup_vendorcompat,
    lib_fixups_user_type,
    libs_clang_rt_ubsan,
    libs_proto_3_9_1,
    libs_proto_21_12,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    "device/nubia/nx659j",
    "hardware/qcom-caf/sm8250",
    "hardware/qcom-caf/wlan",
    "vendor/qcom/opensource/dataservices",
    "vendor/qcom/opensource/display",
    "vendor/nubia/nx659j",
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    libs_clang_rt_ubsan: lib_fixup_remove_arch_suffix,
    libs_proto_3_9_1: lib_fixup_vendorcompat,
    libs_proto_21_12: lib_fixup_remove_proto_version_suffix,
    (
        'libprotobuf-cpp-lite',
        'libprotobuf-cpp-full',
    ): lib_fixup_vendorcompat,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'vendor.qti.imsrtpservice@3.0',
    ): lib_fixup_vendor_suffix,
    (
        'libOmxCore',
        'libgrallocutils',
        'libwpa_client',
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    'system_ext/lib64/lib-imsvideocodec.so': blob_fixup()
        .add_needed('libgui_shim.so'),

    'vendor/bin/dspservice': blob_fixup()
        .remove_needed('libhwbinder.so'),
    'vendor/bin/vppservice': blob_fixup()
        .remove_needed('libhwbinder.so'),
    'vendor/lib64/lib-imsrcs-v2.so': blob_fixup()
        .remove_needed('libhwbinder.so'),
    'vendor/lib/libOmxVpp.so': blob_fixup()
        .remove_needed('libhwbinder.so'),
    'vendor/lib/libvppclient.so': blob_fixup()
        .remove_needed('libhwbinder.so'),

    'vendor/lib64/hw/camera.qcom.so': blob_fixup()
        .add_needed('libcomparetf2.so')
        .replace_needed('libc++.so', 'libc++-v28.so')
        .replace_needed('libsnsapi.so', 'libsnsapi-v28.so'),
        
     'vendor/lib64/android.hardware.camera.provider@2.4-legacy.so': blob_fixup()
        .add_needed("libcamera_provider_shim.so"),   

    'vendor/lib64/camera/components/com.qti.camx.chiiqutils.so': blob_fixup()
        .replace_needed('libsnsapi.so', 'libsnsapi-v28.so'),
    'vendor/lib64/camera/components/com.qti.node.eisv2.so': blob_fixup()
        .replace_needed('libsnsapi.so', 'libsnsapi-v28.so'),
    'vendor/lib64/camera/components/com.qti.node.eisv3.so': blob_fixup()
        .replace_needed('libsnsapi.so', 'libsnsapi-v28.so'),
    'vendor/lib64/libcamera_nn_stub.so': blob_fixup()
        .replace_needed('libsnsapi.so', 'libsnsapi-v28.so'),

    'vendor/lib/hw/fingerprint.goodix_fod.default.so': blob_fixup()
        .set_soname('fingerprint.goodix_fod.default.so')
        .replace_needed('libhidlbase.so', 'libhidlbase-v32.so'),
    'vendor/lib64/hw/fingerprint.goodix_fod.default.so': blob_fixup()
        .set_soname('fingerprint.goodix_fod.default.so')
        .replace_needed('libhidlbase.so', 'libhidlbase-v32.so'),

    'vendor/lib64/libwvhidl.so': blob_fixup()
        .add_needed('libcrypto_shim.so'),
    'vendor/lib64/mediadrm/libwvdrmengine.so': blob_fixup()
        .add_needed('libcrypto_shim.so'),
}  # fmt: skip


module = ExtractUtilsModule(
    'nx659j',
    'nubia',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    check_elf=False,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()

