package com.natan.imageclassifier

import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.Response
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part

interface ApiService {
    @Multipart
    @POST("upload-image/")
    suspend fun uploadImage(
        @Part file: MultipartBody.Part
    ): Response<UploadResponse>
}

data class UploadResponse(
    val message: String?,
    val filename: String?,
    val original_name: String?,
    val file_size: Int?,
    val file_path: String?,
    val error: String?
) 