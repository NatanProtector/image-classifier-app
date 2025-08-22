package com.natan.imageclassifier

import android.net.Uri
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.layout.Arrangement.Absolute.spacedBy
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.lifecycleScope
import coil.compose.AsyncImage
import coil.request.ImageRequest
import kotlinx.coroutines.launch

class ImagePreviewActivity : ComponentActivity() {
    private var imageUri: Uri? = null
    private var source: String = "unknown"
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val imageUriString = intent.getStringExtra("image_uri")
        imageUri = imageUriString?.let { Uri.parse(it) }
        source = intent.getStringExtra("source") ?: "unknown"
        
        setContent {
            ImagePreviewScreen(
                imageUri = imageUri,
                source = source,
                onAccept = { acceptImage() },
                onReject = { rejectImage() }
            )
        }
    }
    
    private fun acceptImage() {
        imageUri?.let { uri ->
            lifecycleScope.launch {
                try {
                    val result = ImageUploader.uploadImage(this@ImagePreviewActivity, uri)
                    result.fold(
                        onSuccess = { uploadResponse ->
                            Toast.makeText(
                                this@ImagePreviewActivity,
                                "Image uploaded successfully: ${uploadResponse.filename}",
                                Toast.LENGTH_LONG
                            ).show()
                            finish()
                        },
                        onFailure = { exception ->
                            Toast.makeText(
                                this@ImagePreviewActivity,
                                "Upload failed: ${exception.message}",
                                Toast.LENGTH_LONG
                            ).show()
                        }
                    )
                } catch (e: Exception) {
                    Toast.makeText(
                        this@ImagePreviewActivity,
                        "Error: ${e.message}",
                        Toast.LENGTH_LONG
                    ).show()
                }
            }
        } ?: run {
            Toast.makeText(this, "No image to upload", Toast.LENGTH_SHORT).show()
        }
    }
    
    private fun rejectImage() {
        finish()
    }
}

@Composable
fun ImagePreviewScreen(
    imageUri: Uri?,
    source: String,
    onAccept: () -> Unit,
    onReject: () -> Unit
) {
    var isUploading by remember { mutableStateOf(false) }
    
    MaterialTheme {
        Surface(
            modifier = Modifier.fillMaxSize()
        ) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(16.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = spacedBy(24.dp)
            ) {
                Spacer(modifier = Modifier.height(16.dp))
                
                // Header with source info
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(
                        text = "Image Preview",
                        fontSize = 24.sp,
                        fontWeight = androidx.compose.ui.text.font.FontWeight.Bold
                    )
                    
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    // Show source information
                    Text(
                        text = "Source: ${source.replaceFirstChar { it.uppercase() }}",
                        fontSize = 16.sp,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                // Image display
                imageUri?.let { uri ->
                    AsyncImage(
                        model = ImageRequest.Builder(LocalContext.current)
                            .data(uri)
                            .crossfade(true)
                            .build(),
                        contentDescription = "Selected image",
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(300.dp),
                        contentScale = ContentScale.Fit
                    )
                } ?: run {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(300.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = "No image to display",
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
                
                Spacer(modifier = Modifier.height(32.dp))
                
                // Action buttons
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = spacedBy(16.dp)
                ) {
                    Button(
                        onClick = onReject,
                        modifier = Modifier
                            .weight(1f)
                            .height(56.dp),
                        colors = ButtonDefaults.buttonColors(
                            containerColor = MaterialTheme.colorScheme.error
                        ),
                        enabled = !isUploading
                    ) {
                        Text(
                            text = "Reject",
                            fontSize = 16.sp
                        )
                    }
                    
                    Button(
                        onClick = {
                            isUploading = true
                            onAccept()
                        },
                        modifier = Modifier
                            .weight(1f)
                            .height(56.dp),
                        enabled = !isUploading
                    ) {
                        if (isUploading) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(24.dp),
                                color = MaterialTheme.colorScheme.onPrimary
                            )
                        } else {
                            Text(
                                text = "Upload",
                                fontSize = 16.sp
                            )
                        }
                    }
                }
                
                Spacer(modifier = Modifier.weight(1f))
            }
        }
    }
} 