package com.natan.imageclassifier

import android.net.Uri
import android.os.Bundle
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import coil.request.ImageRequest

class ImagePreviewActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val imageUriString = intent.getStringExtra("image_uri")
        val imageUri = imageUriString?.let { Uri.parse(it) }
        
        setContent {
            ImagePreviewScreen(
                imageUri = imageUri,
                onAccept = { acceptImage() },
                onReject = { rejectImage() }
            )
        }
    }
    
    private fun acceptImage() {
        // For now, nothing happens with the accepted image
        // You can add your image processing logic here later
        // This could include:
        // - Saving the image to permanent storage
        // - Sending to image classification service
        // - Processing the image for analysis
        finish()
    }
    
    private fun rejectImage() {
        // For now, just go back to previous screen
        // The temporary file will be cleaned up automatically
        finish()
    }
}

@Composable
fun ImagePreviewScreen(
    imageUri: Uri?,
    onAccept: () -> Unit,
    onReject: () -> Unit
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
                verticalArrangement = spacedBy(24.dp)
            ) {
                Spacer(modifier = Modifier.height(32.dp))
                
                Text(
                    text = "Image Preview",
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Bold
                )
                
                Text(
                    text = "Review your image before proceeding",
                    fontSize = 14.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                
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
                        )
                    ) {
                        Text(
                            text = "Reject",
                            fontSize = 16.sp
                        )
                    }
                    
                    Button(
                        onClick = onAccept,
                        modifier = Modifier
                            .weight(1f)
                            .height(56.dp)
                    ) {
                        Text(
                            text = "Accept",
                            fontSize = 16.sp
                        )
                    }
                }
                
                Spacer(modifier = Modifier.weight(1f))
            }
        }
    }
} 