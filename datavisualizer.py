# 2D Data Visualizer

import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

numbers: list = []
check_replace_type: list = []
xcol_check: list = []
ycol_check: list = []
paired: list = []
input_filename: list = []


def main():
    print("2D Data Visualizer\nSelect one of the following options:")
    print("Save | Reset | Load | View | Add | Remove | Edit | Stat | Graph")
    for i in numbers:
        xcol_check.append(i["xval"])
        ycol_check.append(i["yval"])
        paired.append((i["xval"],i["yval"]))
    menu_selection = input("\nSelect: ").lower().strip()
    while True:
        while True:
            if menu_selection == "save":
                save()
                break
            elif menu_selection == "reset":
                reset()
                break
            elif menu_selection == "load":
                try:
                    load(collect_filename())
                except FileNotFoundError:
                    print(f"\nThere is no file named '{input_filename[0]}' in the directory.")
                    break
                break
            elif menu_selection == "view":
                view()
                break
            elif menu_selection == "add":
                add()
                break
            elif menu_selection == "remove":
                rm()
                break
            elif menu_selection == "edit":
                edit()
                break
            elif menu_selection == "stat":
                stat()
                break
            elif menu_selection == "graph":
                graph()
                break
            elif menu_selection == "help" or menu_selection == "-h" or menu_selection == "--help":
                helper()
                break
            else:
                break
        print("\nSelect one of the following options:")
        print("Save | Reset | Load | View | Add | Remove | Edit | Stat | Graph")
        menu_selection = input("\nSelect: ").lower().strip()


# Save the dataset to a new file
def save():
    with open("2ddatavisualizer.csv", "w", newline="\n") as file:
        writer = csv.DictWriter(file,fieldnames=["xval","yval"])
        writer.writeheader()
        for data in numbers:
            writer.writerow({"xval":data["xval"],"yval":data["yval"]})
        print("\nThe file successfully saved as '2ddatavisualizer.csv'.")


# Clear all data from the dataset
def reset():
    reset_input = input("Reset will remove all data from the dataset. Confirm selection (Y/n): ").lower().strip()
    while True:
        if reset_input == "y" or reset_input == "yes":
            print("\nThe dataset has been cleared.")
            numbers.clear()
            xcol_check.clear()
            ycol_check.clear()
            paired.clear()
            return None
        elif reset_input == "n" or reset_input == "no":
            print("\nNo changes have been made.")
            break
        else:
            reset_input = input("Reset will remove all data from the dataset. Confirm selection (Y/n): ").lower().strip()


# Collect file input
def collect_filename():
    load_filename = input("Enter filename: ").strip()
    input_filename.clear()
    input_filename.append(load_filename)
    return load_filename


# Imports CSV or TXT files
def load(filename):
    temp_pair_list: list = []
    try:
        with open(filename, "r") as file:
            reader = csv.reader(file)
            # Skip headers for data validation
            try:
                next(reader)
            except StopIteration:
                no_data = ("The file contains no data.")
                pass
            # Accept CSV and TXT files
            if filename[-3:] == "csv" or filename[-3:] == "txt":
                pass
            else:
                print(f"\n'{filename}' failed to upload.\nImport a CSV or TXT file.")
                return None
            for row in reader:
                if "." in row:
                    select_type = float
                else:
                    select_type = int
                # Temporary list for removing partial failed uploads
                temp_pair_list.append(((select_type(row[0]),select_type(row[1]))))
                rollback = (len(temp_pair_list))
                # Insert data sorted as X, Y, XY, and key value list
                numbers.append({"xval":select_type(row[0]),"yval":select_type(row[1])})
                xcol_check.append(select_type(row[0]))
                ycol_check.append(select_type(row[1]))
                paired.append((select_type(row[0]),select_type(row[1])))
            print(f"\n'{filename}' successfully uploaded.")
            try:
                print(no_data)
            except UnboundLocalError:
                pass
            return [row for row in reader]
    except ValueError:
        print(f"\n'{filename}' failed to fully upload.")
        print("The file must contain an equal number of rows containing numeric data.")
        # Remove partial upload
        try:
            for i in range(1,rollback+1):
                numbers.pop()
                xcol_check.pop()
                ycol_check.pop()
                paired.pop()
        except UnboundLocalError:
            pass
        pass
    except IndexError:
        print(f"\n'{filename}' failed to fully upload.")
        print("The file must contain an equal number of rows containing numeric data.")
        try:
            for i in range(1,rollback+1):
                numbers.pop()
                xcol_check.pop()
                ycol_check.pop()
                paired.pop()
        except UnboundLocalError:
            pass
        pass


# Displays current data
def view():
    if not numbers:
        print("\nThere is no data to display.\nSelect 'Add' or 'Load' to insert data.")
    else:
        print("\nCurrent Data:")
        print(*paired)


# Add ordered pairs
def add():
    add_xvalue = input("Enter X Value: ").strip()
    add_yvalue = input("Enter Y Value: ").strip()
    if "." in add_xvalue:
        select_xtype = float
    else:
        select_xtype = int
    if "." in add_yvalue:
        select_ytype = float
    else:
        select_ytype = int
    try:
        # Sort data as X, Y, XY, and key value list
        xcol_check.append(select_xtype(add_xvalue))
        ycol_check.append(select_ytype(add_yvalue))
        paired.append((select_xtype(add_xvalue),select_ytype(add_yvalue)))
        numbers.append({"xval":select_xtype(add_xvalue),"yval":select_ytype(add_yvalue)})
        print(f"\n{select_xtype(add_xvalue),select_ytype(add_yvalue)} was successfully added.")
        return select_xtype(add_xvalue),select_ytype(add_yvalue)
    except ValueError:
        print("\nX and Y values must be numeric.")
        pass
    # Remove true x when the y creates a ValueError
    if len(xcol_check) == len(ycol_check):
        pass
    elif len(xcol_check) > len(ycol_check):
        xcol_check.pop()


# Remove ordered pairs
def rm():
    if not numbers:
        print("\nThere is no data to remove.\nSelect 'Add' or 'Load' to insert data.")
    else:
        remove_xvalue = input("Enter X Value: ").strip()
        remove_yvalue = input("Enter Y Value: ").strip()
        if "." in remove_xvalue:
            select_xtype = float
        else:
            select_xtype = int
        if "." in remove_yvalue:
            select_ytype = float
        else:
            select_ytype = int
        # Ordered pairs
        for pair in paired:
            try:
                if (select_xtype(remove_xvalue),select_ytype(remove_yvalue)) in paired:
                    xcol_check.remove(select_xtype(remove_xvalue))
                    ycol_check.remove(select_ytype(remove_yvalue))
                    paired.remove((select_xtype(remove_xvalue),select_ytype(remove_yvalue)))
                    # Overwrite the main list
                    numbers.clear()
                    for new in xcol_check,ycol_check:
                        for i in range(len(xcol_check)):
                            try:
                                numbers.append({"xval":xcol_check[i], "yval":ycol_check[i]})
                            except IndexError:
                                break
                        break
                    print(f"\n{select_xtype(remove_xvalue),select_ytype(remove_yvalue)} has been successfully removed.")
                    return select_xtype(remove_xvalue),select_ytype(remove_yvalue)
            except ValueError:
                print("\nOnly numeric values are valid.")
                break
            else:
                print(f"\n{select_xtype(remove_xvalue),select_ytype(remove_yvalue)} does not exist.")
                print("No changes have been made.")
                break


# Edit ordered pairs
def edit():
    if not numbers:
        print("\nThere is no data to edit.\nSelect 'Add' or 'Load' to insert data.")
    else:
        select_xvalue = input("Enter X Value: ").strip()
        select_yvalue = input("Enter Y Value: ").strip()
        if "." in select_xvalue:
            select_xtype_edit = float
        else:
            select_xtype_edit = int
        if "." in select_yvalue:
            select_ytype_edit = float
        else:
            select_ytype_edit = int
        # Ordered pairs list
        for pair in paired:
            try:
                if (select_xtype_edit(select_xvalue),select_ytype_edit(select_yvalue)) in paired:
                    edit_selection = input("Edit X or Y: ").lower().strip()
                    while True:
                        if edit_selection == "x":
                            while True:
                                new_xvalue = input("Enter New X Value: ").strip()
                                # Format selection
                                if "." in new_xvalue:
                                    select_type = float
                                else:
                                    select_type = int
                                try:
                                    # Search the paired list for the ordered pair's index location
                                    index = paired.index((select_xtype_edit(select_xvalue),select_ytype_edit(select_yvalue)))
                                    numbers[index] = {"xval":select_type(new_xvalue),"yval":select_ytype_edit(select_yvalue)}
                                    xcol_check[index] = select_type(new_xvalue)
                                    paired[index] = select_type(new_xvalue),select_ytype_edit(select_yvalue)
                                    break
                                except ValueError:
                                    break
                            print(f"\n{select_xtype_edit(select_xvalue),select_ytype_edit(select_yvalue)} has successfully updated to {select_type(new_xvalue),select_ytype_edit(select_yvalue)}.")
                            return select_type(new_xvalue),select_ytype_edit(select_yvalue)
                        elif edit_selection == "y":
                            while True:
                                new_yvalue = input("Enter New Y Value: ").strip()
                                # Format selection
                                if "." in new_yvalue:
                                    select_type = float
                                else:
                                    select_type = int
                                try:
                                    # Search the paired list for the ordered pair's index location
                                    index = paired.index((select_xtype_edit(select_xvalue),select_ytype_edit(select_yvalue)))
                                    numbers[index] = {"xval":select_xtype_edit(select_xvalue),"yval":select_type(new_yvalue)}
                                    ycol_check[index] = select_type(new_yvalue)
                                    paired[index] = select_xtype_edit(select_xvalue),select_type(new_yvalue)
                                    break
                                except ValueError:
                                    break
                            print(f"\n{select_xtype_edit(select_xvalue),select_ytype_edit(select_yvalue)} has successfully updated to {select_xtype_edit(select_xvalue),select_type(new_yvalue)}.")
                            return select_xtype_edit(select_xvalue),select_type(new_yvalue)
                        else:
                            edit_selection = input("Edit X or Y: ").lower().strip()
            except ValueError:
                print("\nOnly numeric values are valid.")
                break
            else:
                print(f"\n{select_xtype_edit(select_xvalue),select_ytype_edit(select_yvalue)} does not exist.")
                print("No changes have been made.")
                break


# X and Y statistics
def stat():
    if not numbers:
        print("\nThere is no data to display.\nSelect 'Add' or 'Load' to insert data.")
    else:
        try:
            print("\nX Value Statistics")
            print(f"Count: {len(xcol_check)}")
            print(f"Sum: {sum(xcol_check)}")
            print(f"Mean: {round(np.mean(xcol_check),2)}")
            print(f"Median: {np.median(xcol_check)}")
            print(f"Mode: {stats.mode(xcol_check)[0]}")
            print(f"Minimum: {np.min(xcol_check)}")
            print(f"Maximum: {np.max(xcol_check)}")
        except TypeError:
            print("X values statistics will not be displayed with string values.")
            pass
        try:
            print("\nY Value Statistics")
            print(f"Count: {len(ycol_check)}")
            print(f"Sum: {sum(ycol_check)}")
            print(f"Mean: {round(np.mean(ycol_check),2)}")
            print(f"Median: {np.median(ycol_check)}")
            print(f"Mode: {stats.mode(ycol_check)[0]}")
            print(f"Minimum: {np.min(ycol_check)}")
            print(f"Maximum: {np.max(ycol_check)}")
        except TypeError:
            print("Y values statistics will not be displayed with string values.")
            pass


# Graph Data
def graph():
    print("\nVisualizations:\nBar | Hexbin | Histogram | Line | Pie | Scatter | Stack | Stem | Step")
    graph_option = input("\nSelect Visualization: ").lower().strip()
    while True:
        # Bar
        if graph_option == "bar":
            if len(xcol_check) == 0 or len(ycol_check) == 0:
                print("\nThere is no data to display.\nSelect 'Add' or 'Load' to insert data.")
                break
            else:
                # Labels cannot be blank
                bar_chart_title = input("Enter Title: ").strip()
                while True:
                    if bar_chart_title.isspace() or bar_chart_title == "":
                        bar_chart_title = input("Enter Title: ").strip()
                    else:
                        break
                bar_chart_xlabel = input("Enter X Label: ").strip()
                while True:
                    if bar_chart_xlabel.isspace() or bar_chart_xlabel == "":
                        bar_chart_xlabel = input("Enter X Label: ").strip()
                    else:
                        break
                bar_chart_ylabel = input("Enter Y Label: ").strip()
                while True:
                    if bar_chart_ylabel.isspace() or bar_chart_ylabel == "":
                        bar_chart_ylabel = input("Enter Y Label: ").strip()
                    else:
                        break
                try:
                    plt.bar(xcol_check,ycol_check)
                    plt.title(bar_chart_title)
                    plt.xlabel(bar_chart_xlabel)
                    plt.ylabel(bar_chart_ylabel)
                    plt.show()
                    break
                except ValueError:
                    print("\nX and Y must have the same number of values.")
                    break
        # Hexbin
        elif graph_option == "hexbin":
            if len(xcol_check) == 0 or len(ycol_check) == 0:
                print("\nThere is no data to display.\nSelect 'Add' or 'Load' to insert data.")
                break
            else:
                # Labels cannot be blank
                hexbin_plot_title = input("Enter Title: ").strip()
                while True:
                    if hexbin_plot_title.isspace() or hexbin_plot_title == "":
                        hexbin_plot_title = input("Enter Title: ").strip()
                    else:
                        break
                hexbin_plot_xlabel = input("Enter X Label: ").strip()
                while True:
                    if hexbin_plot_xlabel.isspace() or hexbin_plot_xlabel == "":
                        hexbin_plot_xlabel = input("Enter X Label: ").strip()
                    else:
                        break
                hexbin_plot_ylabel = input("Enter Y Label: ").strip()
                while True:
                    if hexbin_plot_ylabel.isspace() or hexbin_plot_ylabel == "":
                        hexbin_plot_ylabel = input("Enter Y Label: ").strip()
                    else:
                        break
                try:
                    plt.hexbin(xcol_check,ycol_check)
                    plt.title(hexbin_plot_title)
                    plt.xlabel(hexbin_plot_xlabel)
                    plt.ylabel(hexbin_plot_ylabel)
                    plt.show()
                    break
                except ValueError:
                    print("\nX and Y must be numeric and have the same size.")
                    break 
        # Histogram
        elif graph_option == "histogram":
            if len(xcol_check) == 0 or len(ycol_check) == 0:
                print("\nThere is no data to display.\nSelect 'Add' or 'Load' to insert data.")
                break
            else:
                select_hist_values = input("Select X or Y values: ").lower().strip()
                while True:
                    if select_hist_values == "x":
                        entered_hist_value = xcol_check
                        break
                    elif select_hist_values == "y":
                        entered_hist_value = ycol_check
                        break
                    else:
                        select_hist_values = input("Select X or Y values: ").lower().strip()
                # Labels cannot be blank
                hist_title = input("Enter Title: ").strip()
                while True:
                    if hist_title.isspace() or hist_title == "":
                        hist_title = input("Enter Title: ").strip()
                    else:
                        break     
                hist_xlabel = input("Enter X Label: ").strip()
                while True:
                    if hist_xlabel.isspace() or hist_xlabel == "":
                        hist_xlabel = input("Enter X Label: ").strip()
                    else:
                        break
                hist_ylabel = input("Enter Y Label: ").strip()
                while True:
                    if hist_ylabel.isspace() or hist_ylabel == "":
                        hist_ylabel = input("Enter Y Label: ").strip()
                    else:
                        break
                plt.hist(entered_hist_value)
                plt.title(hist_title)
                plt.xlabel(hist_xlabel)
                plt.ylabel(hist_ylabel)
                plt.show()
                break
        # Line
        elif graph_option == "line":
            if len(xcol_check) == 0 or len(ycol_check) == 0:
                print("\nThere is no data to display.\nSelect 'Add' or 'Load' to insert data.")
                break
            else:
                # Labels cannot be blank
                line_chart_title = input("Enter Title: ").strip()
                while True:
                    if line_chart_title.isspace() or line_chart_title == "":
                        line_chart_title = input("Enter Title: ").strip()
                    else:
                        break
                line_chart_xlabel = input("Enter X Label: ").strip()
                while True:
                    if line_chart_xlabel.isspace() or line_chart_xlabel == "":
                        line_chart_xlabel = input("Enter X Label: ").strip()
                    else:
                        break
                line_chart_ylabel = input("Enter Y Label: ").strip()
                while True:
                    if line_chart_ylabel.isspace() or line_chart_ylabel == "":
                        line_chart_ylabel = input("Enter Y Label: ").strip()
                    else:
                        break
                try:
                    plt.plot(xcol_check,ycol_check)
                    plt.title(line_chart_title)
                    plt.xlabel(line_chart_xlabel)
                    plt.ylabel(line_chart_ylabel)
                    plt.show()
                    break
                except ValueError:
                    print("\nX and Y must have the same number of values.")
                    break
        # Pie
        elif graph_option == "pie":
            if len(xcol_check) == 0 or len(ycol_check) == 0:
                print("\nThere is no data to display.\nSelect 'Add' or 'Load' to insert data.")
                break
            else:
                # Store added input labels
                store_pie_labels = []
                select_pie_values = input("Select X or Y values: ").lower().strip()
                while True:
                    if select_pie_values == "x":
                        val_choice = xcol_check
                        break
                    elif select_pie_values == "y":
                        val_choice = ycol_check
                        break
                    else:
                        select_pie_values = input("Select X or Y values: ").lower().strip()       
                print(f"\n{len(val_choice)} labels are required. Begin entering labels.")
                print("The main menu can be accessed by entering 'exit'.")
                while True:
                    for i in range(len(val_choice)):
                        for label in val_choice:
                            pie_labels = input(f"Enter label for '{val_choice[i]}': ").strip()
                            if pie_labels == "exit":
                                return
                            while True:
                                if pie_labels.isspace() or pie_labels == "":
                                    pie_labels = input(f"Enter label for '{val_choice[i]}': ").strip()
                                    if pie_labels == "exit":
                                        return
                                else:
                                    break
                            store_pie_labels.append(pie_labels)
                            break
                        if i == len(val_choice):
                            break
                    break
                pie_chart_title = input("Enter Title: ")
                while True:
                    if pie_chart_title.isspace() or pie_chart_title == "":
                        pie_chart_title = input("Enter Title: ")
                    else:
                        break
                try:
                    plt.pie(val_choice, labels=store_pie_labels)
                    plt.title(pie_chart_title)
                    plt.legend()
                    plt.show()
                    break
                except ValueError:
                    print("\nValues must be numeric.")
                    break
        # Scatter
        elif graph_option == "scatter":
            if len(xcol_check) == 0 or len(ycol_check) == 0:
                print("\nThere is no data to display.\nSelect 'Add' or 'Load' to insert data.")
                break
            else:
                # Labels cannot be blank
                scatter_plot_title = input("Enter Title: ").strip()
                while True:
                    if scatter_plot_title.isspace() or scatter_plot_title == "":
                        scatter_plot_title = input("Enter Title: ").strip()
                    else:
                        break
                scatter_plot_xlabel = input("Enter X Label: ").strip()
                while True:
                    if scatter_plot_xlabel.isspace() or scatter_plot_xlabel == "":
                        scatter_plot_xlabel = input("Enter X Label: ").strip()
                    else:
                        break
                scatter_plot_ylabel = input("Enter Y Label: ").strip()
                while True:
                    if scatter_plot_ylabel.isspace() or scatter_plot_ylabel == "":
                        scatter_plot_ylabel = input("Enter Y Label: ").strip()
                    else:
                        break
                try:
                    plt.scatter(xcol_check,ycol_check)
                    plt.title(scatter_plot_title)
                    plt.xlabel(scatter_plot_xlabel)
                    plt.ylabel(scatter_plot_ylabel)
                    plt.show()
                    break
                except ValueError:
                    print("\nX and Y must have the same number of values.")
                    break
        # Stack
        elif graph_option == "stack":
            if len(xcol_check) == 0 or len(ycol_check) == 0:
                print("\nThere is no data to display.\nSelect 'Add' or 'Load' to insert data.")
                break
            else:
                # Labels cannot be blank
                stack_plot_title = input("Enter Title: ").strip()
                while True:
                    if stack_plot_title.isspace() or stack_plot_title == "":
                        stack_plot_title = input("Enter Title: ").strip()
                    else:
                        break
                stack_plot_xlabel = input("Enter X Label: ").strip()
                while True:
                    if stack_plot_xlabel.isspace() or stack_plot_xlabel == "":
                        stack_plot_xlabel = input("Enter X Label: ").strip()
                    else:
                        break
                stack_plot_ylabel = input("Enter Y Label: ").strip()
                while True:
                    if stack_plot_ylabel.isspace() or stack_plot_ylabel == "":
                        stack_plot_ylabel = input("Enter Y Label: ").strip()
                    else:
                        break
                try:
                    plt.stackplot(xcol_check,ycol_check)
                    plt.title(stack_plot_title)
                    plt.xlabel(stack_plot_xlabel)
                    plt.ylabel(stack_plot_ylabel)
                    plt.show()
                    break
                except TypeError:
                    print("\nValues must be numeric.")
                    break
                except ValueError:
                    print("\nX and Y must have the same number of values.")
                    break
        # Stem
        elif graph_option == "stem":
            if len(xcol_check) == 0 or len(ycol_check) == 0:
                print("\nThere is no data to display.\nSelect 'Add' or 'Load' to insert data.")
                break
            else:
                # Labels cannot be blank
                stem_plot_title = input("Enter Title: ").strip()
                while True:
                    if stem_plot_title.isspace() or stem_plot_title == "":
                        stem_plot_title = input("Enter Title: ").strip()
                    else:
                        break
                stem_plot_xlabel = input("Enter X Label: ").strip()
                while True:
                    if stem_plot_xlabel.isspace() or stem_plot_xlabel == "":
                        stem_plot_xlabel = input("Enter X Label: ").strip()
                    else:
                        break
                stem_plot_ylabel = input("Enter Y Label: ").strip()
                while True:
                    if stem_plot_ylabel.isspace() or stem_plot_ylabel == "":
                        stem_plot_ylabel = input("Enter Y Label: ").strip()
                    else:
                        break
                plt.stem(xcol_check,ycol_check)
                plt.title(stem_plot_title)
                plt.xlabel(stem_plot_xlabel)
                plt.ylabel(stem_plot_ylabel)
                plt.show()
                break
        # Step
        elif graph_option == "step":
            if len(xcol_check) == 0 or len(ycol_check) == 0:
                print("\nThere is no data to display.\nSelect 'Add' or 'Load' to insert data.")
                break
            else:
                # Labels cannot be blank
                step_title = input("Enter Title: ").strip()
                while True:
                    if step_title.isspace() or step_title == "":
                        step_title = input("Enter Title: ").strip()
                    else:
                        break
                step_xlabel = input("Enter X Label: ").strip()
                while True:
                    if step_xlabel.isspace() or step_xlabel == "":
                        step_xlabel = input("Enter X Label: ").strip()
                    else:
                        break
                step_ylabel = input("Enter Y Label: ").strip()
                while True:
                    if step_ylabel.isspace() or step_ylabel == "":
                        step_ylabel = input("Enter Y Label: ").strip()
                    else:
                        break
                try:
                    plt.step(xcol_check,ycol_check)
                    plt.title(step_title)
                    plt.xlabel(step_xlabel)
                    plt.ylabel(step_ylabel)
                    plt.show()
                    break
                except TypeError:
                    print("\nX and Y are both required.")
                    break
                except ValueError:
                    print("\nX and Y must have the same number of values.")
                    break
        else:
            print("\nVisualizations:\nBar | Hexbin | Histogram | Line | Pie | Scatter | Stack | Stem | Step")
            graph_option = input("\nSelect Visualization: ").lower().strip()


# Helper guide
def helper():
    print("\n2D Graph Visualizer's Help Guide:\n")
    print(f"Save: {" "*3}Saves the dataset as a new file named '2ddatavisualizer.csv'.")
    print(f"Reset: {" "*2}A reset will remove all data from the dataset.")
    print(f"Load: {" "*3}Imports data from the first two columns of a CSV or TXT file.")
    print(f"{" "*9}The columns must contain headers and a matching number of rows.")
    print(f"{" "*9}The X and Y headers can have any name.")
    print(f"{" "*9}Each import accumulates data and does not overwrite.")
    print(f"View: {" "*3}Displays the current ordered pairs within the dataset.")
    print(f"Add: {" "*4}Add a new ordered pair to the dataset.")
    print(f"Remove: {" "*1}Remove an ordered pair from the dataset.")
    print(f"{" "*9}The first occurrence of duplicate pairs will be removed.")
    print(f"Edit: {" "*3}Edit an X or Y value in an ordered pair.")
    print(f"{" "*9}The first occurrence of duplicate pairs will be altered.")
    print(f"Stat: {" "*3}Displays separate statistics for both X and Y values.")
    print(f"{" "*8} The mode displays the smallest number if all values are unique.")
    print(f"Graph: {" "*2}Opens the graph menu and generates a visualization from the selection.")


if __name__ == "__main__":
    main()