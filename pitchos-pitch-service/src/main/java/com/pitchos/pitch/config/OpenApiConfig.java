package com.pitchos.pitch.config;

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
                        .title("PitchOS - Pitch Management Service API")
                        .description("Tài liệu đặc tả RESTful API cho Dịch vụ Quản lý Sân bóng (Pitch Service - Port 8082). " +
                                "Phụ trách: Linh (Kiến trúc SOA & RESTful API). " +
                                "Hỗ trợ xác thực phân quyền qua JWT Bearer Token với các vai trò: admin, chusan, user.")
                        .version("1.0.0")
                        .contact(new Contact()
                                .name("PitchOS Development Team - Linh (Backend & API Designer)")
                                .email("linh@pitchos.vn"))
                        .license(new License().name("Apache 2.0").url("https://springdoc.org")))
                .addSecurityItem(new SecurityRequirement().addList(securitySchemeName))
                .components(new Components()
                        .addSecuritySchemes(securitySchemeName,
                                new SecurityScheme()
                                        .name(securitySchemeName)
                                        .type(SecurityScheme.Type.HTTP)
                                        .scheme("bearer")
                                        .bearerFormat("JWT")
                                        .description("Nhập chuỗi JWT Token (không cần gõ tiền tố 'Bearer ') để xác thực quyền chusan / admin")));
    }
}
