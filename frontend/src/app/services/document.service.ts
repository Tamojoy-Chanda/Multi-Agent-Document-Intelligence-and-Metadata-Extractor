import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface DocumentResponse {
  id: number;
  filename: string;
  category: string;
  metadata: any;
  message: string;
}

export interface DocumentRecord {
  id: number;
  filename: string;
  category: string;
  metadata_json: any;
  created_at: string;
}

@Injectable({
  providedIn: 'root'
})
export class DocumentService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  uploadDocument(file: File): Observable<DocumentResponse> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<DocumentResponse>(`${this.apiUrl}/upload`, formData);
  }

  getDocuments(): Observable<DocumentRecord[]> {
    return this.http.get<DocumentRecord[]>(`${this.apiUrl}/documents`);
  }
}
