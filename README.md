# Astarte ESP32 SDK

Astarte ESP32 SDK lets you connect your ESP32 device to
[Astarte](https://github.com/astarte-platform/astarte).

The SDK simplifies all the low-level operations like credentials generation, pairing and so on, and
exposes a high-level API to publish data from your device.

Have a look at the [examples](examples/README.md) for a usage example showing how to send and
receive data.

## Documentation

The generated Doxygen documentation is available on the [Astarte Documentation
website](https://docs.astarte-platform.org/1.0/device-sdks/esp32).

## `esp-idf` version compatibility

The SDK is tested against these versions of `esp-idf`:
- `v3.3.4` (only `make` supported)
- `v4.2` (`make` and `idf.py` supported)
- `v5.0` (`idf.py` supported)

Previous versions of `esp-idf` are not guaranteed to work. If you find a problem using a later
version of `esp-idf`, please [open an
issue](https://github.com/astarte-platform/astarte-device-sdk-esp32/issues).

## Notes on non-volatile memory (NVM)

The device's Astarte credentials are always stored in the NVM. This means that credentials will
be preserved in between reboots.

Two storage methods can be used for the credentials. A FAT32 file system or the standard
non-volatile storage (NVS) library provided by the ESP32. The FAT32 is the default storage choice.
If you want to use NVS storage, add the
`astarte_credentials_use_nvs_storage` function before initializing `astarte_credentials`.
```C
astarte_credentials_use_nvs_storage(NVS_PARTITION);
```

As a side effect of NVM usage, credentials will be preserved also between device flashes using
`make` or `idf.py`.

**N.B.** The device will first check if valid credentials are stored in the NVM, and only in case
of a negative result will use the `Astarte SDK` component configuration to obtain fresh credentials.

Most of the time during development the device credentials remain unchanged between firmware
flashes and the old ones stored in the NVM can be reused.
However, when changing elements of the `Astarte SDK` component configuration the old credentials
should be discarded by erasing the NMV.
This can be done using the following command:
| ESP-IDF $\geqslant$ v4.x | ESP-IDF v3.x |
| ------------- | ------------ |
| `idf.py -p <DEVICE_PORT> erase-flash` | `make ESPPORT=<DEVICE_PORT> erase_flash` |
