import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { API_URL } from '../env';
import { Exam } from './exam.model';

@Injectable()
export class DocumentApiService {

  constructor(private http: HttpClient) {
  }

  // init dictionary
  initDocDict(): Observable<any> {
    return this.http.get<any>(`${API_URL}/init`).pipe(
      catchError((error: any) => {
        console.error("Error found when initializing dictionaries for documents", error);
        return throwError("Error occurred while initializing dictionaries for documents");
      })
    );
  }

  // fetch the documents
  initDoc(filename: string): Observable<string> {
    return this.http.get<DocText>(`${API_URL}/initial_text/${filename}`).pipe(
        map((response: DocText) => { return response.content ?? ""; }),
        catchError((error: any) => {
            console.error("Error found when initializing document: ", error);
            return new Observable<string>();
        })
    );
  }
}
interface DocText {
    content?: string,
    error?: string
}