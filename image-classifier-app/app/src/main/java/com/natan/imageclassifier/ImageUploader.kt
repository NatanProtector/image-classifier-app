package com.natan.imageclassifier

import android.content.Context
import android.net.Uri
import android.util.Log
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody
import java.io.File
import java.io.FileOutputStream

class ImageUploader {
    companion object {
        private const val TAG = "ImageUploader"
        
        suspend fun uploadImage(context: Context, imageUri: Uri): Result<UploadResponse> {
            return withContext(Dispatchers.IO) {
                try {
                    // Convert URI to File
                    val file = uriToFile(context, imageUri)
                    if (file == null) {
                        return@withContext Result.failure(Exception("Failed to convert URI to file"))
                    }
                    
                    // Create multipart request body
                    val requestBody = file.asRequestBody("image/*".toMediaTypeOrNull())
                    val multipartBody = MultipartBody.Part.createFormData("file", file.name, requestBody)
                    
                    // Upload to server
                    val response = NetworkClient.apiService.uploadImage(multipartBody)
                    
                    if (response.isSuccessful) {
                        response.body()?.let { uploadResponse ->
                            if (uploadResponse.error != null) {
                                Result.failure(Exception(uploadResponse.error))
                            } else {
                                Result.success(uploadResponse)
                            }
                        } ?: Result.failure(Exception("Empty response body"))
                    } else {
                        Result.failure(Exception("Upload failed: ${response.code()} ${response.message()}"))
                    }
                } catch (e: Exception) {
                    Log.e(TAG, "Error uploading image", e)
                    Result.failure(e)
                }
            }
        }
        
        private fun uriToFile(context: Context, uri: Uri): File? {
            return try {
                val inputStream = context.contentResolver.openInputStream(uri)
                val file = File(context.cacheDir, "temp_image_${System.currentTimeMillis()}.jpg")
                val outputStream = FileOutputStream(file)
                
                inputStream?.use { input ->
                    outputStream.use { output ->
                        input.copyTo(output)
                    }
                }
                
                file
            } catch (e: Exception) {
                Log.e(TAG, "Error converting URI to file", e)
                null
            }
        }
    }
} 