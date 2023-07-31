import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { API_URL } from '../env';

@Injectable()
export class DocumentApiService {

  constructor(private http: HttpClient) {
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

  // search text in the documents
  searchText(filename: string, searchText: string): Observable<SearchResult> {
    return this.http.get<SearchResult>(`${API_URL}/search_text/${filename}/${searchText}`).pipe(
      map((response: SearchResult) => {return response ?? new Observable<SearchResult>();}),
      catchError((error: any) => {
        console.error("Error found when initializing document: ", error);
        return new Observable<SearchResult>();
    })
    );
  }
}
interface DocText {
    content?: string,
    error?: string
}

export interface Occurrence {
  line: number;
  start: number;
  end: number;
  in_sentence: string;
}

export interface SearchResult {
  query_text?: string,
  number_of_occurrences?: string,
  occurences?: Occurrence[],
  error?: string
}