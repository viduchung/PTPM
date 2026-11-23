package com.pitchos.pitch.dto;

import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Thông tin định danh instance phục vụ request của Pitch Service")
public class InstanceInfoResponse {

    @Schema(description = "Tên dịch vụ đã đăng ký với Service Registry", example = "pitchos-pitch-service")
    private String serviceName;

    @Schema(description = "Mã định danh duy nhất của instance", example = "pitch-instance-1")
    private String instanceId;

    @Schema(description = "Cổng mạng instance đang lắng nghe", example = "8082")
    private int port;

    public InstanceInfoResponse() {
    }

    public InstanceInfoResponse(String serviceName, String instanceId, int port) {
        this.serviceName = serviceName;
        this.instanceId = instanceId;
        this.port = port;
    }

    public static InstanceInfoResponseBuilder builder() {
        return new InstanceInfoResponseBuilder();
    }

    public String getServiceName() {
        return serviceName;
    }

    public void setServiceName(String serviceName) {
        this.serviceName = serviceName;
    }

    public String getInstanceId() {
        return instanceId;
    }

    public void setInstanceId(String instanceId) {
        this.instanceId = instanceId;
    }

    public int getPort() {
        return port;
    }

    public void setPort(int port) {
        this.port = port;
    }

    public static class InstanceInfoResponseBuilder {
        private String serviceName;
        private String instanceId;
        private int port;

        public InstanceInfoResponseBuilder serviceName(String serviceName) {
            this.serviceName = serviceName;
            return this;
        }

        public InstanceInfoResponseBuilder instanceId(String instanceId) {
            this.instanceId = instanceId;
            return this;
        }

        public InstanceInfoResponseBuilder port(int port) {
            this.port = port;
            return this;
        }

        public InstanceInfoResponse build() {
            return new InstanceInfoResponse(serviceName, instanceId, port);
        }
    }
}
