package com.pitchos.pitch.controller;

import com.pitchos.pitch.dto.InstanceInfoResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Tag(name = "0. Định danh Instance (Instance Info)", description = "API tra cứu định danh instance đang phục vụ nhằm kiểm thử cân bằng tải và giám sát container")
public class InstanceInfoController {

    private static final Logger log = LoggerFactory.getLogger(InstanceInfoController.class);

    @Value("${spring.application.name:pitchos-pitch-service}")
    private String serviceName;

    @Value("${INSTANCE_ID:${pitchos.instance-id:pitch-default}}")
    private String instanceId;

    @Value("${server.port:8082}")
    private int port;

    @Operation(summary = "Lấy thông tin định danh instance phục vụ",
               description = "Trả về serviceName, instanceId và port thực tế để xác minh instance nào đang nhận xử lý request qua Spring Cloud LoadBalancer.")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Lấy thông tin instance thành công",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = InstanceInfoResponse.class)))
    })
    @GetMapping({"/api/v1/instance-info", "/api/v1/pitches/instance-info"})
    public ResponseEntity<InstanceInfoResponse> getInstanceInfo() {
        log.info("[{}] Nhận request GET instance-info - Đang phục vụ trên port {}", instanceId, port);
        InstanceInfoResponse response = InstanceInfoResponse.builder()
                .serviceName(serviceName)
                .instanceId(instanceId)
                .port(port)
                .build();
        return ResponseEntity.ok(response);
    }
}
