import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { ExamsApiService } from './exam/exam-api.service';
import { DocumentApiService } from './exam/document-api.service';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
  ],
  providers: [
    ExamsApiService, 
    DocumentApiService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
