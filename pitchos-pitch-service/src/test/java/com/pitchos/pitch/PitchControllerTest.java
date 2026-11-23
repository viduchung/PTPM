package com.pitchos.pitch;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.pitchos.pitch.dto.CreatePitchRequest;
import com.pitchos.pitch.dto.UpdatePitchStatusRequest;
import com.pitchos.pitch.entity.PitchStatus;
import com.pitchos.pitch.entity.PitchType;
import com.pitchos.pitch.security.JwtUtil;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;

import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest(properties = {
        "spring.datasource.url=jdbc:h2:mem:pitchos_pitch_db;DB_CLOSE_DELAY=-1;MODE=MySQL;DATABASE_TO_LOWER=TRUE",
        "spring.datasource.driver-class-name=org.h2.Driver",
        "spring.datasource.username=sa",
        "spring.datasource.password=",
        "spring.jpa.hibernate.ddl-auto=create-drop",
        "spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.H2Dialect"
})
@AutoConfigureMockMvc
@ActiveProfiles("h2")
@Transactional
public class PitchControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private JwtUtil jwtUtil;

    // Token mẫu ký bằng secret key chuẩn
    private String getChusanToken() {
        return jwtUtil.generateTestToken("chusan", 2L, "chusan", 3600000L);
    }

    private String getUserToken() {
        return jwtUtil.generateTestToken("user", 3L, "user", 3600000L);
    }

    @Test
    @DisplayName("Ca 1: GET /api/v1/pitches công khai không cần token -> 200 OK và có danh sách sân")
    void testGetAllPitches_Public_Success() throws Exception {
        mockMvc.perform(get("/api/v1/pitches"))
                .andExpect(status().isOk())
                .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$", hasSize(greaterThanOrEqualTo(4))))
                .andExpect(jsonPath("$[0].name", notNullValue()))
                .andExpect(jsonPath("$[0].pricePerHour", notNullValue()));
    }

    @Test
    @DisplayName("Ca 2: GET /api/v1/pitches/1 lấy chi tiết sân -> 200 OK")
    void testGetPitchById_Success() throws Exception {
        mockMvc.perform(get("/api/v1/pitches/1"))
                .andExpect(status().isOk())
                .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.id", is(1)))
                .andExpect(jsonPath("$.name", is("Sân bóng Mini Tiểu Ngư")))
                .andExpect(jsonPath("$.status", is("hoat_dong")));
    }

    @Test
    @DisplayName("Ca 3: GET /api/v1/pitches/99999 sân không tồn tại -> 404 Not Found")
    void testGetPitchById_NotFound() throws Exception {
        mockMvc.perform(get("/api/v1/pitches/99999"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status", is(404)))
                .andExpect(jsonPath("$.error", is("Not Found")))
                .andExpect(jsonPath("$.message", containsString("Không tìm thấy sân bóng")));
    }

    @Test
    @DisplayName("Ca 4 (Bảo mật 401): POST /api/v1/pitches không gửi token -> 401 Unauthorized")
    void testCreatePitch_NoToken_Unauthorized() throws Exception {
        CreatePitchRequest req = new CreatePitchRequest(
                "Sân Test", PitchType.san_5, new BigDecimal("300000.00"),
                "Hà Nội", null, null
        );

        mockMvc.perform(post("/api/v1/pitches")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.status", is(401)))
                .andExpect(jsonPath("$.error", is("Unauthorized")))
                .andExpect(jsonPath("$.message", containsString("Chưa xác thực danh tính")));
    }

    @Test
    @DisplayName("Ca 5 (Bảo mật 403): POST /api/v1/pitches dùng token role user -> 403 Forbidden")
    void testCreatePitch_UserRole_Forbidden() throws Exception {
        CreatePitchRequest req = new CreatePitchRequest(
                "Sân Test", PitchType.san_5, new BigDecimal("300000.00"),
                "Hà Nội", null, null
        );

        mockMvc.perform(post("/api/v1/pitches")
                        .header("Authorization", "Bearer " + getUserToken())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.status", is(403)))
                .andExpect(jsonPath("$.error", is("Forbidden")))
                .andExpect(jsonPath("$.message", containsString("không đủ quyền")));
    }

    @Test
    @DisplayName("Ca 6 (Validation 400): POST /api/v1/pitches token chusan nhưng dữ liệu sai (tên trống, giá âm) -> 400 Bad Request")
    void testCreatePitch_Validation_BadRequest() throws Exception {
        CreatePitchRequest invalidReq = new CreatePitchRequest(
                "", // Tên trống vi phạm @NotBlank
                PitchType.san_5,
                new BigDecimal("-500000.00"), // Giá âm vi phạm @Positive
                "", // Địa chỉ trống vi phạm @NotBlank
                null, null
        );

        mockMvc.perform(post("/api/v1/pitches")
                        .header("Authorization", "Bearer " + getChusanToken())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(invalidReq)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status", is(400)))
                .andExpect(jsonPath("$.error", is("Bad Request")))
                .andExpect(jsonPath("$.errors.name", containsString("Tên sân bóng không được để trống")))
                .andExpect(jsonPath("$.errors.pricePerHour", containsString("phải lớn hơn 0")))
                .andExpect(jsonPath("$.errors.address", containsString("Địa chỉ sân không được để trống")));
    }

    @Test
    @DisplayName("Ca 7 (Thành công 201): POST /api/v1/pitches token chusan và dữ liệu chuẩn -> 201 Created")
    void testCreatePitch_ChusanRole_Created() throws Exception {
        CreatePitchRequest validReq = new CreatePitchRequest(
                "Sân bóng Hàng Đẫy VIP",
                PitchType.san_7,
                new BigDecimal("600000.00"),
                "Số 9 Trịnh Hoài Đức, Đống Đa, Hà Nội",
                "https://images.unsplash.com/photo-1529900240041-22f1df4d0a11",
                "https://maps.google.com/?q=21.0285,105.8342"
        );

        mockMvc.perform(post("/api/v1/pitches")
                        .header("Authorization", "Bearer " + getChusanToken())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(validReq)))
                .andExpect(status().isCreated())
                .andExpect(header().exists("Location"))
                .andExpect(jsonPath("$.id", notNullValue()))
                .andExpect(jsonPath("$.name", is("Sân bóng Hàng Đẫy VIP")))
                .andExpect(jsonPath("$.pitchType", is("san_7")))
                .andExpect(jsonPath("$.status", is("hoat_dong")));
    }

    @Test
    @DisplayName("Ca 8: PATCH /api/v1/pitches/1/status token chusan -> 200 OK cập nhật trạng thái")
    void testUpdatePitchStatus_Success() throws Exception {
        UpdatePitchStatusRequest req = new UpdatePitchStatusRequest(PitchStatus.bao_tri);

        mockMvc.perform(patch("/api/v1/pitches/1/status")
                        .header("Authorization", "Bearer " + getChusanToken())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id", is(1)))
                .andExpect(jsonPath("$.status", is("bao_tri")));
    }
}
