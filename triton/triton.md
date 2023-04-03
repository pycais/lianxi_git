# core

```
git clone https://github.com/triton-inference-server/core.git -b r22.05
```

# third_party

```
git clone https://github.com/triton-inference-server/third_party.git -b r22.05
```

## curl

```
git clone https://github.com/curl/curl.git -b curl-7_66_0
# 没有依赖
```

## grpc-repo

```
git clone https://github.com/grpc/grpc.git -b v1.25.0 grpc-repo
```

### abseil-cpp

```
wget https://github.com/abseil/abseil-cpp/archive/74d91756c11bc22f9b0108b94da9326f7f9e376f.zip
# 没有依赖
```

### benckmark

```
wget https://github.com/google/benchmark/archive/6cf20f1e0219078371161af83319d10f72f0832e.zip
修改出：benchmark/cmake/GoogleTest.cmake: 55行
改成：set(GOOGLETEST_PATH "/tmp/tritonbuild/tritonserver/install/grpc-repo/third_party/googletest") 
```

### googletest

```
wget https://github.com/google/googletest/archive/c9ccac7cb7345901884aabf5d1a786cfa6e2f397.zip
```

### googleapis

```
wget https://github.com/googleapis/googleapis/archive/80ed4d0bbf65d57cc267dfc63bd2584557f11f9b.zip
```

### bloaty

```
wget https://github.com/google/bloaty/archive/73594cde8c9a52a102c4341c244c833aa61b9c06.zip
```

### boringssl

```
wget https://github.com/google/boringssl/archive/7f02881e96e51f1873afcf384d02f782b48967ca.zip
# 没有依赖
```

### boringssl-with-bazel

```
wget https://github.com/google/boringssl/archive/83da28a68f32023fd3b95a8ae94991a07b1f6c62.zip
```

### cares

```
wget https://github.com/c-ares/c-ares/archive/e982924acee7f7313b4baa4ee5ec000c5e373c30.zip
# 没有依赖
```

### envoy-api

```
wget https://github.com/envoyproxy/data-plane-api/archive/c181f78882e54c0e5c63f332562ef6954ee7932f.zip
```

### gflags

```
wget https://github.com/gflags/gflags/archive/28f50e0fed19872e0fd50dd23ce2ee8cd759338e.zip
```

#### doc

```
wget https://github.com/gflags/gflags/archive/8411df715cf522606e3b1aca386ddfc0b63d34b4.zip
```

### protobuf

```
wget https://github.com/protocolbuffers/protobuf/archive/09745575a923640154bcf307fba8aedff47f240a.zip
```

### protoc-gen-validate

```
wget https://github.com/bufbuild/protoc-gen-validate/archive/e143189bf6f37b3957fb31743df6a1bcf4a8c685.zip
```

### udpa

```
wget https://github.com/cncf/udpa/archive/94324803a497c8f76dbc78df393ef629d3a9f3c3.zip
```



### zlib

```
wget https://github.com/madler/zlib/archive/cacf7f1d4e3d44d871b605da3b647f07d718623f.zip
```







## gprc-repo-new

```
git clone https://github.com/grpc/grpc.git -b v1.29.1 grpc-repo-new
```

## json

```
git clone https://github.com/nlohmann/json.git -b v3.9.0
# 没有依赖
```

## libevent

```
git clone https://github.com/libevent/libevent.git -b release-2.1.8-stable
```

## prometheus-cpp

```
wget https://github.com/jupp0r/prometheus-cpp/archive/v0.7.0.tar.gz

```

## crc32c

```
git clone https://github.com/google/crc32c.git
git checkout b9d6e825a1e6783195a6051639179152dac70b3b
```

## google-cloud-cpp

```
git clone https://github.com/googleapis/google-cloud-cpp.git -b v1.23.0
```

## azure-storage-cpplite

```
git clone https://github.com/Azure/azure-storage-cpplite.git -b v0.3.0
```

## aws-sdk-cpp

```
git clone https://github.com/aws/aws-sdk-cpp.git -b 1.8.186
```







