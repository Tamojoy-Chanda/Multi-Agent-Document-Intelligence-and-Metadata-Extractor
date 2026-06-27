import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DocumentService, DocumentRecord } from './services/document.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  documents: DocumentRecord[] = [];
  isUploading = false;
  uploadError = '';
  selectedFile: File | null = null;

  constructor(private documentService: DocumentService) {}

  ngOnInit(): void {
    this.loadDocuments();
  }

  loadDocuments(): void {
    this.documentService.getDocuments().subscribe({
      next: (docs) => {
        this.documents = docs;
      },
      error: (err) => {
        console.error('Error fetching documents', err);
      }
    });
  }

  onFileSelected(event: any): void {
    const file: File = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      this.selectedFile = file;
      this.uploadError = '';
    } else {
      this.selectedFile = null;
      this.uploadError = 'Please select a valid PDF file.';
    }
  }

  onUpload(): void {
    if (!this.selectedFile) return;

    this.isUploading = true;
    this.uploadError = '';

    this.documentService.uploadDocument(this.selectedFile).subscribe({
      next: (response) => {
        this.isUploading = false;
        this.selectedFile = null;
        // Reset file input
        const fileInput = document.getElementById('file-upload') as HTMLInputElement;
        if (fileInput) fileInput.value = '';
        
        // Reload documents to show the new one
        this.loadDocuments();
      },
      error: (err) => {
        this.isUploading = false;
        console.error('Upload failed', err);
        this.uploadError = 'Upload failed. Please try again.';
      }
    });
  }

  // Helper method to format metadata object to a nice string
  formatMetadata(metadata: any): string {
    if (!metadata) return '';
    try {
      const parsed = typeof metadata === 'string' ? JSON.parse(metadata) : metadata;
      return Object.keys(parsed)
        .map(key => `${key.replace(/_/g, ' ')}: ${parsed[key]}`)
        .join(' | ');
    } catch (e) {
      return JSON.stringify(metadata);
    }
  }
}
