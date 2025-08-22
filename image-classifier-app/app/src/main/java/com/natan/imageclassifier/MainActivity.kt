package com.natan.imageclassifier

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.layout.Arrangement.Absolute.spacedBy
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import androidx.core.content.FileProvider
import java.io.File

class MainActivity : ComponentActivity() {
    private var photoFile: File? = null
    
    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { isGranted: Boolean ->
        if (isGranted) {
            // Permission granted, can proceed with camera
            takePhoto()
        }
    }

    private val cameraLauncher = registerForActivityResult(
        ActivityResultContracts.TakePicture()
    ) { success ->
        if (success) {
            // Photo was taken successfully, launch image preview
            photoFile?.let { file ->
                val photoUri = FileProvider.getUriForFile(
                    this,
                    "${packageName}.fileprovider",
                    file
                )
                val intent = Intent(this, ImagePreviewActivity::class.java).apply {
                    putExtra("image_uri", photoUri.toString())
                }
                startActivity(intent)
            }
        }
    }

    private val galleryLauncher = registerForActivityResult(
        ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        uri?.let { selectedImageUri ->
            // Launch image preview activity
            val intent = Intent(this, ImagePreviewActivity::class.java).apply {
                putExtra("image_uri", selectedImageUri.toString())
            }
            startActivity(intent)
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MainScreen(
                onTakeImageClick = { openCamera() },
                onUploadImageClick = { openGallery() }
            )
        }
    }

    private fun openCamera() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) 
            == PackageManager.PERMISSION_GRANTED) {
            takePhoto()
        } else {
            requestPermissionLauncher.launch(Manifest.permission.CAMERA)
        }
    }

    private fun takePhoto() {
        createImageFile()
        photoFile?.let { file ->
            val photoUri = FileProvider.getUriForFile(
                this,
                "${packageName}.fileprovider",
                file
            )
            cameraLauncher.launch(photoUri)
        }
    }

    private fun createImageFile(): File {
        val timeStamp = java.text.SimpleDateFormat("yyyyMMdd_HHmmss", java.util.Locale.getDefault()).format(java.util.Date())
        val storageDir = getExternalFilesDir(null)
        return File.createTempFile(
            "JPEG_${timeStamp}_",
            ".jpg",
            storageDir
        ).apply {
            photoFile = this
        }
    }

    private fun openGallery() {
        galleryLauncher.launch("image/*")
    }
}

@Composable
fun MainScreen(
    onTakeImageClick: () -> Unit,
    onUploadImageClick: () -> Unit
) {
    MaterialTheme {
        Surface(
            modifier = Modifier.fillMaxSize()
        ) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(16.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = spacedBy(32.dp)
            ) {
                Spacer(modifier = Modifier.height(64.dp))
                
                Text(
                    text = "Natan's Image Classifier",
                    fontSize = 28.sp,
                    fontWeight = FontWeight.Bold
                )
                
                Spacer(modifier = Modifier.height(64.dp))
                
                Button(
                    onClick = onTakeImageClick,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(56.dp)
                ) {
                    Text(
                        text = "Take Image",
                        fontSize = 18.sp
                    )
                }
                
                Button(
                    onClick = onUploadImageClick,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(56.dp)
                ) {
                    Text(
                        text = "Upload Image",
                        fontSize = 18.sp
                    )
                }
                
                Spacer(modifier = Modifier.weight(1f))
            }
        }
    }
}