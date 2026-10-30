package com.pitchos.auth.config;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        final String securitySchemeName = "BearerAuth";

        return new OpenAPI()
                .info(new Info()
                        .title("PitchOS - Auth & User Service API")
                        .description("Tài liệu đặc tả RESTful API cho Dịch vụ Xác thực và Người dùng (Auth Service - Port 8081). "
                                + "Phụ trách: Hoàng (Nhóm trưởng - Bảo mật JWT & Phân quyền RBAC). "
                                + "Cấp phát Bearer JWT Token dùng chung cho toàn hệ thống với 3 vai trò: admin, chusan, user.")
                        .version("1.0.0")
                        .contact(new Contact()
                                .name("PitchOS Development Team - Hoàng (Security Architect)")
                                .email("hoang@pitchos.vn"))
                        .license(new License().name("Apache 2.0").url("https://springdoc.org")))
                .addSecurityItem(new SecurityRequirement().addList(securitySchemeName))
                .components(new Components()
                        .addSecuritySchemes(securitySchemeName,
                                new SecurityScheme()
                                        .name(securitySchemeName)
                                        .type(SecurityScheme.Type.HTTP)
                                        .scheme("bearer")
                                        .bearerFormat("JWT")
                                        .description("Nhập chuỗi JWT Token lấy từ API POST /api/v1/auth/login "
                                                + "(không cần gõ tiền tố 'Bearer ')")));
    }
}
