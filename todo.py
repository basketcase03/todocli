import sys
import argparse
import os
from datetime import datetime

class MyParser(argparse.ArgumentParser):
    def print_usage(self,message):
        print('''Usage :-
$ ./todo add "todo item"  # Add a new todo
$ ./todo ls               # Show remaining todos
$ ./todo del NUMBER       # Delete a todo
$ ./todo done NUMBER      # Complete a todo
$ ./todo help             # Show usage
$ ./todo report           # Statistics''')
        sys.exit()

    def print_help(self, message):
        print_usage(self,message)
        sys.exit()
    

def write_file(path,data):
    f = open(path,'w')
    f.write(data)
    f.close()

def create_files():
    todo = os.path.join(os.getcwd(), 'todo.txt')
    done = os.path.join(os.getcwd(), 'done.txt')

    if not os.path.isfile(todo):
        write_file(todo,'')
    if not os.path.isfile(done):
        write_file(done,'')

def add_(args):
    txt = args.additem+'\n'
    todo = os.path.join(os.getcwd(), 'todo.txt')
    with open(todo, "a") as myfile:
        myfile.write(txt)
    print('Added todo: "{line_}"'.format(line_=txt.rstrip()))
    

def ls_(args):
    todo = os.path.join(os.getcwd(), 'todo.txt')
    with open(todo, "r") as myfile:
        todolist=myfile.readlines()
        if(len(todolist)==0):
            print("There are no pending todos!")
        for i,item in enumerate(reversed(todolist)):
            txt='[{counter}] '+item.rstrip()
            print(txt.format(counter=len(todolist)-i))

def del_(args):
    todo = os.path.join(os.getcwd(), 'todo.txt')
    with open(todo, "r") as myfile:
        lines = myfile.readlines()
        if args.delitem-1 >= len(lines) or args.delitem<1:
            print("Error: todo #{i} does not exist. Nothing deleted.".format(i=args.delitem))
            return
    with open(todo,"w") as myfile:
        for i,line in enumerate(lines):
            if i!=(args.delitem-1):
                myfile.write(line)
    print("Deleted todo #{i}".format(i=args.delitem))    

def done_(args):
    todoitem=''

    todo = os.path.join(os.getcwd(), 'todo.txt')
    with open(todo, "r") as myfile:
        lines = myfile.readlines()
        if args.doneitem > len(lines) or args.doneitem<1:
            print("Error: todo #{i} does not exist.".format(i=args.doneitem))
            return
    with open(todo,"w") as myfile:
        for i,line in enumerate(lines):
            if i!=args.doneitem-1:
                myfile.write(line)
            else:
                todoitem=line

    date = datetime.today().strftime('%Y-%m-%d')
    txt = 'x '+date+' '+todoitem

    done = os.path.join(os.getcwd(), 'done.txt')
    with open(done,"a") as myfile:
        myfile.write(txt)
    print("Marked todo #{i} as done.".format(i=args.doneitem))


    


def help_(args):
    print('''Usage :-
$ ./todo add "todo item"  # Add a new todo
$ ./todo ls               # Show remaining todos
$ ./todo del NUMBER       # Delete a todo
$ ./todo done NUMBER      # Complete a todo
$ ./todo help             # Show usage
$ ./todo report           # Statistics''')
    

def report_(args):
    pend=0
    comp=0
    todo = os.path.join(os.getcwd(), 'todo.txt')
    with open(todo, "r") as myfile:
        lines = myfile.readlines()
        pend=len(lines)

    done = os.path.join(os.getcwd(), 'done.txt')
    with open(done, "r") as myfile:
        lines = myfile.readlines()
        comp=len(lines)

    txt='{date_} Pending : {pend_} Completed : {comp_}'.format(date_= datetime.today().strftime('%Y-%m-%d'),
    pend_= pend,comp_=comp)
    print(txt)

if __name__=='__main__':
    create_files()

    parser = MyParser(prog='TodoList',
              usage='''Usage :-
$ ./todo add "todo item"  # Add a new todo
$ ./todo ls               # Show remaining todos
$ ./todo del NUMBER       # Delete a todo
$ ./todo done NUMBER      # Complete a todo
$ ./todo help             # Show usage
$ ./todo report           # Statistics
              ''',
              formatter_class=argparse.RawDescriptionHelpFormatter,
              add_help=True)

    subparsers = parser.add_subparsers(help='sub-command help')

    parser_add=subparsers.add_parser("add",help="add item",add_help=True)
    parser_add.add_argument('additem',type=str,help='.\\todo add "task"')
    parser_add.set_defaults(func=add_)

    parser_ls=subparsers.add_parser("ls")
    parser_ls.set_defaults(func=ls_)
    
    parser_del=subparsers.add_parser("del",help="Enter id to del")
    parser_del.add_argument('delitem',type=int,help='.\\todo del 2')
    parser_del.set_defaults(func=del_)

    parser_done=subparsers.add_parser("done",help="Enter id that is done")
    parser_done.add_argument('doneitem',type=int,help='.\\todo done 3')
    parser_done.set_defaults(func=done_)

    parser_help=subparsers.add_parser("help")
    parser_help.set_defaults(func=help_)

    parser_report=subparsers.add_parser("report")
    parser_report.set_defaults(func=report_)
    
    if(len(sys.argv)>1):
        if(sys.argv[1]=='add' and len(sys.argv)<3):
            print("Error: Missing todo string. Nothing added!")
            sys.exit()

        elif(sys.argv[1]=='del' and len(sys.argv)<3):
            print("Error: Missing NUMBER for deleting todo.")
            sys.exit()

        elif(sys.argv[1]=='done' and len(sys.argv)<3):
            print("Error: Missing NUMBER for marking todo as done.")
            sys.exit()

    


    args = parser.parse_args()
    if(len(vars(args))==0):
        print('''Usage :-
$ ./todo add "todo item"  # Add a new todo
$ ./todo ls               # Show remaining todos
$ ./todo del NUMBER       # Delete a todo
$ ./todo done NUMBER      # Complete a todo
$ ./todo help             # Show usage
$ ./todo report           # Statistics''')
        sys.exit()
    args.func(args)
