package com.pitchos.booking;

import com.pitchos.booking.client.PitchClient;
import com.pitchos.booking.dto.PitchResponseDTO;
import com.pitchos.booking.exception.ResourceNotFoundException;
import com.pitchos.booking.repository.BookingRepository;
import com.pitchos.booking.support.TestTokens;
import feign.Request;
import feign.RequestTemplate;
import feign.RetryableException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.context.WebApplicationContext;

import java.math.BigDecimal;
import java.net.SocketTimeoutException;
import java.nio.charset.StandardCharsets;
import java.util.Collections;
import java.util.Map;

import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.BDDMockito.given;
import static org.mockito.BDDMockito.willThrow;
import static org.springframework.security.test.web.servlet.setup.SecurityMockMvcConfigurers.springSecurity;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * BO KIEM THU TICH HOP IT01 - IT07 (KT2 - Nhat, muc 2.2).
 *
 * Chay Booking Service that (Spring Security + JPA + GlobalExceptionHandler) tren H2 in-memory,
 * chi thay PitchClient bang mock de mo phong moi kieu phan hoi cua Provider: du lieu tot, 404,
 * du lieu rac, het instance trong Eureka, timeout mang.
 *
 * Bo test nay KHONG thay the minh chung Postman tren Docker, ma dung de kiem tra logic tich hop
 * moi luc, ke ca khi Eureka / Pitch Service cua nhom chua khoi dong.
 */
@SpringBootTest
@ActiveProfiles("test")
@DisplayName("IT01-IT07: Consumer goi Provider va xu ly loi tich hop")
class IntegrationErrorHandlingTest {

    private static final long CUSTOMER_ID = 3L;
    private static final long PITCH_ID = 1L;

    @Autowired
    private WebApplicationContext context;

    @Autowired
    private BookingRepository bookingRepository;

    @MockBean
    private PitchClient pitchClient;

    private MockMvc mockMvc;
    private String customerToken;

    @BeforeEach
    void setUp() {
        mockMvc = MockMvcBuilders.webAppContextSetup(context).apply(springSecurity()).build();
        bookingRepository.deleteAll();
        customerToken = TestTokens.bearer(CUSTOMER_ID, "user");
    }

    @Test
    @DisplayName("IT01 - Dat san hop le: 201 Created, totalPrice = so gio x don gia Provider")
    void it01_datSanHopLe() throws Exception {
        given(pitchClient.getPitchById(PITCH_ID))
                .willReturn(pitch(new BigDecimal("300000.00"), "hoat_dong"));

        mockMvc.perform(post("/api/v1/bookings")
                        .header(HttpHeaders.AUTHORIZATION, customerToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(bookingBody(PITCH_ID, "2027-05-01T18:00:00", "2027-05-01T19:30:00")))
                .andExpect(status().isCreated())
                // 1,5 gio x 300.000 = 450.000
                .andExpect(jsonPath("$.totalPrice").value(450000.00))
                .andExpect(jsonPath("$.status").value("cho_duyet"))
                .andExpect(jsonPath("$.userId").value(CUSTOMER_ID));
    }

    @Test
    @DisplayName("IT02 - San khong ton tai (Provider tra 404): Consumer tra 404 kem thong bao ro rang")
    void it02_sanKhongTonTai() throws Exception {
        // CustomErrorDecoder da quy 404 cua Provider thanh ResourceNotFoundException
        willThrow(new ResourceNotFoundException("Khong tim thay san bong voi pitchId da gui"))
                .given(pitchClient).getPitchById(9999L);

        mockMvc.perform(post("/api/v1/bookings")
                        .header(HttpHeaders.AUTHORIZATION, customerToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(bookingBody(9999L, "2027-05-01T18:00:00", "2027-05-01T19:30:00")))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status").value(404))
                .andExpect(jsonPath("$.message").value("Khong tim thay san bong voi pitchId da gui"));
    }

    @Test
    @DisplayName("IT03a - Don gia Provider <= 0: 502 Bad Gateway")
    void it03a_donGiaKhongHopLe() throws Exception {
        given(pitchClient.getPitchById(PITCH_ID)).willReturn(pitch(BigDecimal.ZERO, "hoat_dong"));

        mockMvc.perform(post("/api/v1/bookings")
                        .header(HttpHeaders.AUTHORIZATION, customerToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(bookingBody(PITCH_ID, "2027-05-02T18:00:00", "2027-05-02T19:30:00")))
                .andExpect(status().isBadGateway())
                .andExpect(jsonPath("$.status").value(502));
    }

    @Test
    @DisplayName("IT03b - Don gia Provider null: 502 Bad Gateway")
    void it03b_donGiaNull() throws Exception {
        given(pitchClient.getPitchById(PITCH_ID)).willReturn(pitch(null, "hoat_dong"));

        mockMvc.perform(post("/api/v1/bookings")
                        .header(HttpHeaders.AUTHORIZATION, customerToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(bookingBody(PITCH_ID, "2027-05-02T18:00:00", "2027-05-02T19:30:00")))
                .andExpect(status().isBadGateway());
    }

    @Test
    @DisplayName("IT03c - San dang bao tri: 400 Bad Request (loi nghiep vu, khong phai loi Provider)")
    void it03c_sanBaoTri() throws Exception {
        given(pitchClient.getPitchById(PITCH_ID))
                .willReturn(pitch(new BigDecimal("250000.00"), "bao_tri"));

        mockMvc.perform(post("/api/v1/bookings")
                        .header(HttpHeaders.AUTHORIZATION, customerToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(bookingBody(PITCH_ID, "2027-05-03T18:00:00", "2027-05-03T19:30:00")))
                .andExpect(status().isBadRequest());
    }

    @Test
    @DisplayName("IT04 - Provider sap hoan toan (Eureka het instance): 503, Booking van song")
    void it04_providerSapHoanToan() throws Exception {
        willThrow(new IllegalStateException("No instances available for pitchos-pitch-service"))
                .given(pitchClient).getPitchById(anyLong());

        mockMvc.perform(post("/api/v1/bookings")
                        .header(HttpHeaders.AUTHORIZATION, customerToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(bookingBody(PITCH_ID, "2027-05-04T18:00:00", "2027-05-04T19:30:00")))
                .andExpect(status().isServiceUnavailable())
                .andExpect(jsonPath("$.status").value(503));

        // Chung minh Booking Service KHONG sap theo: endpoint khac van phuc vu binh thuong
        mockMvc.perform(get("/api/v1/bookings/my-bookings")
                        .header(HttpHeaders.AUTHORIZATION, customerToken))
                .andExpect(status().isOk());
    }

    @Test
    @DisplayName("IT05 - Timeout mang khi goi Provider: 503 chu khong phai 500")
    void it05_timeoutMang() throws Exception {
        willThrow(readTimeout()).given(pitchClient).getPitchById(anyLong());

        mockMvc.perform(post("/api/v1/bookings")
                        .header(HttpHeaders.AUTHORIZATION, customerToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(bookingBody(PITCH_ID, "2027-05-05T18:00:00", "2027-05-05T19:30:00")))
                .andExpect(status().isServiceUnavailable())
                .andExpect(jsonPath("$.status").value(503));
    }

    @Test
    @DisplayName("IT06 - Gui lap cung khung gio: lan 1 tra 201, lan 2 tra 400 trung lich")
    void it06_guiLapYeuCau() throws Exception {
        given(pitchClient.getPitchById(PITCH_ID))
                .willReturn(pitch(new BigDecimal("300000.00"), "hoat_dong"));

        String body = bookingBody(PITCH_ID, "2027-05-06T18:00:00", "2027-05-06T19:30:00");

        mockMvc.perform(post("/api/v1/bookings")
                        .header(HttpHeaders.AUTHORIZATION, customerToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(body))
                .andExpect(status().isCreated());

        mockMvc.perform(post("/api/v1/bookings")
                        .header(HttpHeaders.AUTHORIZATION, customerToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(body))
                .andExpect(status().isBadRequest());
    }

    @Test
    @DisplayName("IT07 - endTime truoc startTime: 400 ngay tai tang validation, khong goi Provider")
    void it07_duLieuDauVaoSai() throws Exception {
        mockMvc.perform(post("/api/v1/bookings")
                        .header(HttpHeaders.AUTHORIZATION, customerToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(bookingBody(PITCH_ID, "2027-05-07T20:00:00", "2027-05-07T18:00:00")))
                .andExpect(status().isBadRequest());

        Mockito.verifyNoInteractions(pitchClient);
    }

    @Test
    @DisplayName("TC03 - GET /pitch-instance tra ve instance Provider do LoadBalancer phan phoi")
    void tc03_pitchInstance() throws Exception {
        given(pitchClient.getInstanceInfo())
                .willReturn(Map.of("instanceId", "pitchos-pitch-service:8084", "port", 8084));

        mockMvc.perform(get("/api/v1/bookings/pitch-instance"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.port").value(8084));
    }

    @Test
    @DisplayName("TC05 - GET /pitch-instance khi Provider da dung het: 503 sach se")
    void tc05_pitchInstanceKhiProviderSap() throws Exception {
        willThrow(new IllegalStateException("No instances available for pitchos-pitch-service"))
                .given(pitchClient).getInstanceInfo();

        mockMvc.perform(get("/api/v1/bookings/pitch-instance"))
                .andExpect(status().isServiceUnavailable());
    }

    private PitchResponseDTO pitch(BigDecimal pricePerHour, String status) {
        return new PitchResponseDTO(PITCH_ID, "San Bong Dai Hoc The Thao (San 5)", pricePerHour, status);
    }

    private String bookingBody(long pitchId, String startTime, String endTime) {
        return "{\"pitchId\":" + pitchId
                + ",\"startTime\":\"" + startTime
                + "\",\"endTime\":\"" + endTime + "\"}";
    }

    /** Dung dung ngoai le Feign nem ra khi doc response qua thoi gian cho (read-timeout 3s). */
    private RetryableException readTimeout() {
        Request request = Request.create(Request.HttpMethod.GET,
                "http://pitchos-pitch-service/api/v1/pitches/1",
                Collections.emptyMap(), null, StandardCharsets.UTF_8, new RequestTemplate());
        return new RetryableException(-1, "Read timed out", Request.HttpMethod.GET,
                new SocketTimeoutException("Read timed out"), (Long) null, request);
    }
}
