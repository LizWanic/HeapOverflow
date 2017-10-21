#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <time.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <string.h>
#include <signal.h>

#define MAX_LINES 500       
#define SERVER_PORT 4444

typedef struct _contact {
   char data[256];
   struct _contact *next;
} contact;   

char WELCOME[] = "Welcome to the simple address book (1.0)!\n";

void execute_this() {
   puts("we really should never see this");
}

void printMenu() {
   printf("1) Add contact\n");
   printf("2) Edit contact\n");
   printf("3) Remove contact\n");
   printf("4) List contacts\n");
   printf("5) Save contacts\n");
   printf("6) Load contacts\n");
   printf("7) Quit\n");
}

contact *add() {
   contact *temp = (contact*)calloc(1, sizeof(contact));
   printf("Enter new contact (last,first,email,phone,address)\n");
   fgets(temp->data, sizeof(temp->data), stdin);
   return temp;
}

void insert(contact **head, contact *c) {
   contact *p = NULL, *n;
   for (n = *head; n; n = n->next) {
      if (strcmp(c->data, n->data) <= 0) {
         c->next = n;
         break;
      }
      p = n;
   }
   if (p == NULL) {
      *head = c;
   }
   else {
      p->next = c;
   }
}

void edit(contact **head) {
   char data[256];
   printf("Enter last name to edit\n");
   if (fgets(data, sizeof(data), stdin)) {
      contact *n, *p;
      char *lf = strchr(data, '\n');
      if (lf) {
         *lf = 0;
      }
      p = NULL;
      for (n = *head; n; n = n->next) {
         if (strncmp(n->data, data, strlen(data)) == 0) {
            if (n == *head) {
               *head = n->next;
            }
            if (p) {
               p->next = n->next;
            }
            break;
         }
         p = n;
      }
      if (n) {
         printf("Enter new contact info (last,first,email,phone,address)\n");
         scanf("%s", n->data);
         n->next = NULL;
         contact *p = NULL, *temp;
         for (temp = *head; temp; temp = temp->next) {
            if (strcmp(n->data, temp->data) <= 0) {
               n->next = temp;
               break;
            }
            p = temp;
         }
         if (p == NULL) {
            *head = n;
         }
         else {
            p->next = n;
         }
      }
      else {
         printf("Failed to find contact\n");
      }            
   }
}

void remove_contact(contact **head) {
   char data[256];
   printf("Enter last name to delete\n");
   if (fgets(data, sizeof(data), stdin)) {
      char *lf = strchr(data, '\n');
      contact *n, *p;
      if (lf) {
         *lf = 0;
      }
      p = NULL;
      for (n = *head; n; n = n->next) {
         if (strncmp(n->data, data, strlen(data)) == 0) {
            if (n == *head) {
               *head = n->next;
            }
            if (p) {
               p->next = n->next;
            }
            free(n);
            break;
         }
         p = n;
      }
      if (n == NULL) {
         printf("Failed to find contact %s\n", data);
      }
   }
}

void save(contact **head) {
   char data[256];
   printf("Enter save file name\n");
   if (fgets(data, sizeof(data), stdin)) {
      char *lf = strchr(data, '\n');
      if (lf) {
         *lf = 0;
      }
      FILE *of = fopen(data, "w");
      if (of) {
         contact *n;
         for (n = *head; n; n = n->next) {
            fprintf(of, "%s\n", n->data);
         }
         fclose(of);
      }
      else {
         printf("Failed to open file %s\n", data);
      }
   }
}

void load(contact **head) {
   char data[256];
   printf("Enter load file name\n");
   if (fgets(data, sizeof(data), stdin)) {
      char *lf = strchr(data, '\n');
      if (lf) {
         *lf = 0;
      }
      FILE *of = fopen(data, "r");
      if (of) {
         contact *n, *p;
         for (n = *head; n; n = p) {
            p = n->next;
            free(n);
         }
         *head = NULL;
         contact *temp = (contact*)calloc(1, sizeof(contact));
         while (fgets(temp->data, sizeof(temp->data), of)) {
            if (*head == NULL) {
               *head = n = temp;
            }
            else {
               n->next = temp;
               n = temp;
            }
            temp = (contact*)calloc(1, sizeof(contact));
         }
         free(temp);
         fclose(of);
      }
      else {
         printf("Failed to open file %s\n", data);
      }
   }
}

void service() {
   char data[256];
   contact *contacts = NULL;
   contact *p, *n;
   contact *temp;
   int done = 0;

   printf(WELCOME);
   
   while (!done) {
      printMenu();
      if (fgets(data, sizeof(data), stdin) == NULL) {
         break;
      }
      switch (*data) {
         case '7':
            done = 1;
            break;
         case '1': //add
            temp = add();
            insert(&contacts, temp);
            break;
         case '2': //replace / edit
            edit(&contacts);
            break;
         case '3': {//delete
            remove_contact(&contacts);
            break;
         }
         case '4':  //list / print
            for (n = contacts; n; n = n->next) {
               printf("%s\n", n->data);
            }
            break;
         case '5': { //save
            save(&contacts);
            break;
         }
         case '6': { //load
            load(&contacts);
            break;
         }
      }
   }
   
   //lets free everything up
   for (n = contacts; n; n = p) {
      p = n->next;
      free(n);
   }
}

int main(int argc, char **argv) {   
   signal(SIGCHLD, SIG_IGN);
   setvbuf(stdin, NULL, _IONBF, 0);
   setvbuf(stdout, NULL, _IONBF, 0);
   setvbuf(stderr, NULL, _IONBF, 0);
   service();
}
