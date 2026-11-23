package com.pitchos.booking;

import com.pitchos.booking.client.PitchClient;
import com.pitchos.booking.support.TestTokens;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.context.WebApplicationContext;

import static org.springframework.security.test.web.servlet.setup.SecurityMockMvcConfigurers.springSecurity;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * Phan quyen RBAC va cac endpoint cong khai phuc vu van hanh (KT2).
 * Token khong gui / sai -> 401; sai vai tro -> 403;
 * /actuator/health va /api/v1/bookings/pitch-instance goi duoc khong can token.
 */
@SpringBootTest
@ActiveProfiles("test")
@DisplayName("RBAC va endpoint cong khai (actuator, pitch-instance)")
class SecurityRbacTest {

    private static final String BOOKING_BODY =
            "{\"pitchId\":1,\"startTime\":\"2027-06-01T18:00:00\",\"endTime\":\"2027-06-01T19:30:00\"}";

    @Autowired
    private WebApplicationContext context;

    @MockBean
    private PitchClient pitchClient;

    private MockMvc mockMvc;

    @BeforeEach
    void setUp() {
        mockMvc = MockMvcBuilders.webAppContextSetup(context).apply(springSecurity()).build();
    }

    @Test
    @DisplayName("Khong gui token -> 401 Unauthorized")
    void khongGuiToken() throws Exception {
        mockMvc.perform(post("/api/v1/bookings")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(BOOKING_BODY))
                .andExpect(status().isUnauthorized());
    }

    @Test
    @DisplayName("Token sai vai tro (chusan dat san) -> 403 Forbidden")
    void saiVaiTro() throws Exception {
        mockMvc.perform(post("/api/v1/bookings")
                        .header(HttpHeaders.AUTHORIZATION, TestTokens.bearer(2L, "chusan"))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(BOOKING_BODY))
                .andExpect(status().isForbidden());
    }

    @Test
    @DisplayName("DEP02 - GET /actuator/health khong can token -> 200 UP")
    void actuatorHealthCongKhai() throws Exception {
        mockMvc.perform(get("/actuator/health"))
                .andExpect(status().isOk())
                .andExpect(content().string(org.hamcrest.Matchers.containsString("UP")));
    }
}
